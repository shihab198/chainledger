from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import threading
import json
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkNode:
    """Handles peer-to-peer communication between blockchain nodes"""
    
    def __init__(self, blockchain, host: str = '127.0.0.1', port: int = 5000):
        self.blockchain = blockchain
        self.host = host
        self.port = port
        self.peers: List[str] = []
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask API routes"""
        
        @self.app.route('/ping', methods=['GET'])
        def ping():
            return jsonify({"status": "online", "node_id": self.blockchain.node_id})
        
        @self.app.route('/chain', methods=['GET'])
        def get_chain():
            """Get the full blockchain"""
            return jsonify({
                "length": self.blockchain.get_chain_length(),
                "chain": self.blockchain.to_dict()
            })
        
        @self.app.route('/blocks', methods=['GET'])
        def get_blocks():
            """Get all blocks"""
            blocks = [block.to_dict() for block in self.blockchain.chain]
            return jsonify({"blocks": blocks, "count": len(blocks)})
        
        @self.app.route('/evidence', methods=['POST'])
        def add_evidence():
            """Add new evidence"""
            data = request.get_json()
            result = self.blockchain.add_evidence(
                data['evidence_id'],
                data['description'],
                data['officer'],
                data['location'],
                data['evidence_type'],
                data.get('hash', '')
            )
            
            # Broadcast to peers
            self.broadcast_transaction(result['transaction'])
            
            return jsonify(result)
        
        @self.app.route('/transfer', methods=['POST'])
        def transfer_evidence():
            """Transfer evidence custody"""
            data = request.get_json()
            result = self.blockchain.transfer_evidence(
                data['evidence_id'],
                data['from_officer'],
                data['to_officer'],
                data['reason']
            )
            
            # Broadcast to peers
            self.broadcast_transaction(result['transaction'])
            
            return jsonify(result)
        
        @self.app.route('/evidence/<evidence_id>', methods=['GET'])
        def get_evidence_history(evidence_id):
            """Get history of specific evidence"""
            history = self.blockchain.get_evidence_history(evidence_id)
            return jsonify({"evidence_id": evidence_id, "history": history})
        
        @self.app.route('/evidence/all', methods=['GET'])
        def get_all_evidence():
            """Get all evidence"""
            evidence = self.blockchain.get_all_evidence()
            return jsonify({"evidence": evidence, "count": len(evidence)})
        
        @self.app.route('/validate', methods=['GET'])
        def validate_chain():
            """Validate blockchain integrity"""
            is_valid = self.blockchain.is_chain_valid()
            return jsonify({
                "valid": is_valid,
                "chain_length": self.blockchain.get_chain_length()
            })
        
        @self.app.route('/peers', methods=['GET'])
        def get_peers():
            """Get list of connected peers"""
            return jsonify({"peers": self.peers, "count": len(self.peers)})
        
        @self.app.route('/peers/add', methods=['POST'])
        def add_peer():
            """Add a new peer"""
            data = request.get_json()
            peer_url = data['peer_url']
            if peer_url not in self.peers:
                self.peers.append(peer_url)
                logger.info(f"Added peer: {peer_url}")
            return jsonify({"peers": self.peers})
        
        @self.app.route('/sync', methods=['POST'])
        def sync_chain():
            """Sync blockchain from peers"""
            longest_chain = None
            max_length = self.blockchain.get_chain_length()
            
            for peer in self.peers:
                try:
                    response = requests.get(f"{peer}/chain", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        length = data['length']
                        chain_data = data['chain']
                        
                        if length > max_length:
                            max_length = length
                            longest_chain = chain_data
                except Exception as e:
                    logger.error(f"Error syncing with {peer}: {str(e)}")
            
            if longest_chain:
                self.blockchain.from_dict(longest_chain)
                return jsonify({
                    "message": "Chain synchronized",
                    "new_length": max_length
                })
            
            return jsonify({"message": "Chain is up to date"})
        
        @self.app.route('/transaction/receive', methods=['POST'])
        def receive_transaction():
            """Receive transaction from peer"""
            data = request.get_json()
            transaction = data['transaction']
            
            # Add transaction to blockchain
            self.blockchain.pending_transactions.append(transaction)
            self.blockchain.create_block()
            
            return jsonify({"status": "Transaction received"})
    
    def broadcast_transaction(self, transaction: Dict):
        """Broadcast transaction to all peers"""
        for peer in self.peers:
            try:
                requests.post(
                    f"{peer}/transaction/receive",
                    json={"transaction": transaction},
                    timeout=5
                )
                logger.info(f"Broadcasted transaction to {peer}")
            except Exception as e:
                logger.error(f"Error broadcasting to {peer}: {str(e)}")
    
    def connect_to_peer(self, peer_url: str):
        """Connect to a peer node"""
        # Remove trailing slash
        peer_url = peer_url.rstrip('/')
        
        if peer_url not in self.peers:
            try:
                # Test connection
                response = requests.get(f"{peer_url}/ping", timeout=5)
                if response.status_code == 200:
                    self.peers.append(peer_url)
                    
                    # Register self with peer
                    my_url = f"http://{self.host}:{self.port}"
                    try:
                        requests.post(
                            f"{peer_url}/peers/add",
                            json={"peer_url": my_url},
                            timeout=5
                        )
                    except:
                        pass  # Peer might not support this endpoint
                    
                    logger.info(f"Connected to peer: {peer_url}")
                    return True
                else:
                    logger.error(f"Peer {peer_url} returned status {response.status_code}")
                    return False
            except Exception as e:
                logger.error(f"Failed to connect to {peer_url}: {str(e)}")
                return False
        else:
            logger.info(f"Already connected to {peer_url}")
            return True
    
    def start(self):
        """Start the Flask server"""
        # IMPORTANT: Use 0.0.0.0 to accept connections from other computers
        bind_host = '0.0.0.0' if self.host == '127.0.0.1' else self.host
        
        thread = threading.Thread(
            target=self.app.run,
            kwargs={'host': bind_host, 'port': self.port, 'debug': False, 'use_reloader': False}
        )
        thread.daemon = True
        thread.start()
        logger.info(f"Node started on {bind_host}:{self.port} (accessible from network)")
        return thread