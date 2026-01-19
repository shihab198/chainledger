#!/usr/bin/env python3
"""
ChainLedger Web Application
Complete web-based blockchain chain of custody system
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import time
import threading
from blockchain import Blockchain
from network import NetworkNode


class ChainLedgerWebApp:
    """Web application for ChainLedger"""
    
    def __init__(self, node_id: str, port: int, node_name: str):
        self.node_id = node_id
        self.port = port
        self.node_name = node_name
        
        # Initialize blockchain
        self.blockchain = Blockchain(node_id)
        
        # Create Flask app
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Setup routes
        self.setup_routes()
        
        # Initialize network node (will be started separately)
        self.network = NetworkNode(self.blockchain, port=port)
    
    def setup_routes(self):
        """Setup all web routes"""
        
        @self.app.route('/')
        def index():
            """Main dashboard"""
            return render_template('index.html', 
                                 node_name=self.node_name,
                                 node_id=self.node_id,
                                 port=self.port)
        
        @self.app.route('/api/node/info')
        def node_info():
            """Get node information"""
            return jsonify({
                'node_id': self.node_id,
                'node_name': self.node_name,
                'port': self.port,
                'chain_length': self.blockchain.get_chain_length()
            })
        
        @self.app.route('/api/evidence', methods=['GET', 'POST'])
        def evidence():
            """Handle evidence operations"""
            if request.method == 'POST':
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
                self.network.broadcast_transaction(result['transaction'])
                
                return jsonify(result)
            else:
                evidence = self.blockchain.get_all_evidence()
                return jsonify({'evidence': evidence, 'count': len(evidence)})
        
        @self.app.route('/api/transfer', methods=['POST'])
        def transfer():
            """Transfer evidence custody"""
            data = request.get_json()
            result = self.blockchain.transfer_evidence(
                data['evidence_id'],
                data['from_officer'],
                data['to_officer'],
                data['reason']
            )
            
            # Broadcast to peers
            self.network.broadcast_transaction(result['transaction'])
            
            return jsonify(result)
        
        @self.app.route('/api/evidence/<evidence_id>/history')
        def evidence_history(evidence_id):
            """Get evidence history"""
            history = self.blockchain.get_evidence_history(evidence_id)
            return jsonify({'evidence_id': evidence_id, 'history': history})
        
        @self.app.route('/api/blocks')
        def blocks():
            """Get all blocks"""
            blocks = [block.to_dict() for block in self.blockchain.chain]
            return jsonify({'blocks': blocks, 'count': len(blocks)})
        
        @self.app.route('/api/validate')
        def validate():
            """Validate blockchain"""
            is_valid = self.blockchain.is_chain_valid()
            return jsonify({
                'valid': is_valid,
                'chain_length': self.blockchain.get_chain_length()
            })
        
        @self.app.route('/api/peers', methods=['GET', 'POST'])
        def peers():
            """Manage peers"""
            if request.method == 'POST':
                data = request.get_json()
                peer_url = data['peer_url'].strip()
                
                # Remove trailing slash if present
                if peer_url.endswith('/'):
                    peer_url = peer_url[:-1]
                
                # Add peer directly to network node
                if peer_url not in self.network.peers:
                    self.network.peers.append(peer_url)
                    
                    # Try to ping the peer
                    try:
                        import requests
                        response = requests.get(f"{peer_url}/api/node/info", timeout=3)
                        if response.status_code == 200:
                            # Also register ourselves with the peer
                            my_url = f"http://127.0.0.1:{self.port}"
                            requests.post(
                                f"{peer_url}/api/peers",
                                json={'peer_url': my_url},
                                timeout=3
                            )
                            return jsonify({
                                'success': True,
                                'message': f'Connected to {peer_url}',
                                'peers': self.network.peers
                            })
                        else:
                            return jsonify({
                                'success': False,
                                'message': 'Peer not responding',
                                'peers': self.network.peers
                            })
                    except Exception as e:
                        # Keep peer in list even if connection fails (might come online later)
                        return jsonify({
                            'success': False,
                            'message': f'Error connecting: {str(e)}',
                            'peers': self.network.peers
                        })
                else:
                    return jsonify({
                        'success': True,
                        'message': 'Peer already connected',
                        'peers': self.network.peers
                    })
            else:
                return jsonify({
                    'peers': self.network.peers,
                    'count': len(self.network.peers)
                })
        
        @self.app.route('/api/sync', methods=['POST'])
        def sync():
            """Sync blockchain with peers"""
            import requests
            
            longest_chain = None
            max_length = self.blockchain.get_chain_length()
            synced_from = None
            
            for peer in self.network.peers:
                try:
                    response = requests.get(f"{peer}/api/blocks", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        blocks = data['blocks']
                        length = len(blocks)
                        
                        if length > max_length:
                            max_length = length
                            longest_chain = blocks
                            synced_from = peer
                except Exception as e:
                    print(f"Error syncing with {peer}: {str(e)}")
            
            if longest_chain:
                # Reconstruct blockchain from blocks
                from blockchain import Block
                self.blockchain.chain = [Block.from_dict(b) for b in longest_chain]
                
                # Update database with new blocks
                if self.blockchain.db:
                    for block_dict in longest_chain:
                        self.blockchain.db.save_block(block_dict, self.blockchain.node_id)
                
                return jsonify({
                    'message': f'Chain synchronized from {synced_from}',
                    'new_length': max_length,
                    'synced': True
                })
            
            return jsonify({
                'message': 'Chain is up to date',
                'synced': False
            })
    
    def run(self):
        """Start the web application"""
        print(f"\n{'='*70}")
        print(f"ChainLedger Web Application")
        print(f"{'='*70}")
        print(f"Node: {self.node_name}")
        print(f"URL: http://127.0.0.1:{self.port}")
        print(f"{'='*70}\n")
        
        self.app.run(host='0.0.0.0', port=self.port, debug=False)


def main():
    """Main entry point"""
    nodes = {
        '1': {'id': 'node_a', 'port': 5000, 'name': 'Node A - Officer 1'},
        '2': {'id': 'node_b', 'port': 5001, 'name': 'Node B - Officer 2'},
        '3': {'id': 'node_c', 'port': 5002, 'name': 'Node C - Supervisor'}
    }
    
    if len(sys.argv) != 2 or sys.argv[1] not in nodes:
        print("\nUsage: python app.py [node_number]")
        print("\nAvailable nodes:")
        print("  1 - Node A (Officer 1) - http://127.0.0.1:5000")
        print("  2 - Node B (Officer 2) - http://127.0.0.1:5001")
        print("  3 - Node C (Supervisor) - http://127.0.0.1:5002")
        print("\nExample: python app.py 1\n")
        sys.exit(1)
    
    node_num = sys.argv[1]
    config = nodes[node_num]
    
    app = ChainLedgerWebApp(config['id'], config['port'], config['name'])
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()