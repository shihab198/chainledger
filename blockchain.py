import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: float, data: Dict, 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, block_dict: Dict) -> 'Block':
        """Create block from dictionary"""
        block = cls(
            block_dict['index'],
            block_dict['timestamp'],
            block_dict['data'],
            block_dict['previous_hash'],
            block_dict['nonce']
        )
        block.hash = block_dict['hash']
        return block


class Blockchain:
    """Main blockchain class for chain of custody management"""
    
    def __init__(self, node_id: str, use_database: bool = True):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.node_id = node_id
        self.use_database = use_database
        self.db = None
        
        if use_database:
            from database import BlockchainDatabase
            self.db = BlockchainDatabase(f"chainledger_{node_id}.db")
            self.load_from_database()
        else:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(
            0,
            time.time(),
            {
                "type": "genesis",
                "message": "ChainLedger Genesis Block",
                "node": self.node_id
            },
            "0"
        )
        self.chain.append(genesis_block)
        
        # Save to database if enabled
        if self.db:
            self.db.save_block(genesis_block.to_dict(), self.node_id)
    
    def load_from_database(self):
        """Load blockchain from database"""
        if not self.db:
            return
        
        blocks = self.db.get_all_blocks()
        
        if len(blocks) == 0:
            # No blocks in database, create genesis
            self.create_genesis_block()
        else:
            # Load blocks from database
            self.chain = [Block.from_dict(block_dict) for block_dict in blocks]
            print(f"✓ Loaded {len(self.chain)} blocks from database")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_evidence(self, evidence_id: str, description: str, 
                     officer: str, location: str, evidence_type: str,
                     hash_value: str = "") -> Dict:
        """Add new evidence to the blockchain"""
        transaction = {
            "type": "evidence_creation",
            "evidence_id": evidence_id,
            "description": description,
            "officer": officer,
            "location": location,
            "evidence_type": evidence_type,
            "hash": hash_value or self._generate_evidence_hash(evidence_id, description),
            "action": "Created",
            "timestamp": datetime.now().isoformat(),
            "node": self.node_id
        }
        return self.add_transaction(transaction)
    
    def transfer_evidence(self, evidence_id: str, from_officer: str, 
                          to_officer: str, reason: str) -> Dict:
        """Transfer evidence custody"""
        transaction = {
            "type": "evidence_transfer",
            "evidence_id": evidence_id,
            "from_officer": from_officer,
            "to_officer": to_officer,
            "reason": reason,
            "action": "Transferred",
            "timestamp": datetime.now().isoformat(),
            "node": self.node_id
        }
        return self.add_transaction(transaction)
    
    def add_transaction(self, transaction: Dict) -> Dict:
        """Add a transaction and create a new block"""
        self.pending_transactions.append(transaction)
        new_block = self.create_block()
        return {
            "success": True,
            "block": new_block.to_dict(),
            "transaction": transaction
        }
    
    def create_block(self) -> Block:
        """Create a new block with pending transactions"""
        if not self.pending_transactions:
            return None
        
        new_block = Block(
            len(self.chain),
            time.time(),
            self.pending_transactions.copy(),
            self.get_latest_block().hash
        )
        
        self.chain.append(new_block)
        self.pending_transactions = []
        
        # Save to database if enabled
        if self.db:
            self.db.save_block(new_block.to_dict(), self.node_id)
            self.db.update_node_info(self.node_id, len(self.chain))
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_all_evidence(self) -> List[Dict]:
        """Get all evidence entries"""
        # Use database if available for better performance
        if self.db:
            return self.db.get_all_evidence()
        
        # Fallback to scanning blockchain
        evidence_dict = {}
        
        for block in self.chain[1:]:
            if isinstance(block.data, list):
                for transaction in block.data:
                    evidence_id = transaction.get('evidence_id')
                    if evidence_id:
                        if evidence_id not in evidence_dict:
                            evidence_dict[evidence_id] = {
                                'evidence_id': evidence_id,
                                'description': transaction.get('description', 'N/A'),
                                'type': transaction.get('evidence_type', 'N/A'),
                                'current_officer': transaction.get('officer') or transaction.get('to_officer'),
                                'created': transaction.get('timestamp'),
                                'last_action': transaction.get('action'),
                                'block_index': block.index
                            }
                        else:
                            # Update with latest transfer info
                            if transaction.get('type') == 'evidence_transfer':
                                evidence_dict[evidence_id]['current_officer'] = transaction.get('to_officer')
                                evidence_dict[evidence_id]['last_action'] = transaction.get('action')
        
        return list(evidence_dict.values())
    
    def get_evidence_history(self, evidence_id: str) -> List[Dict]:
        """Get complete history of a specific evidence"""
        # Use database if available
        if self.db:
            return self.db.get_evidence_history(evidence_id)
        
        # Fallback to scanning blockchain
        history = []
        for block in self.chain[1:]:  # Skip genesis block
            if isinstance(block.data, list):
                for transaction in block.data:
                    if transaction.get('evidence_id') == evidence_id:
                        history.append({
                            "block_index": block.index,
                            "timestamp": transaction.get('timestamp'),
                            "action": transaction.get('action'),
                            "officer": transaction.get('officer') or transaction.get('to_officer'),
                            "details": transaction
                        })
        return history
    
    def _generate_evidence_hash(self, evidence_id: str, description: str) -> str:
        """Generate a hash for evidence"""
        content = f"{evidence_id}{description}{time.time()}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert blockchain to dictionary"""
        return {
            "node_id": self.node_id,
            "chain": [block.to_dict() for block in self.chain],
            "pending_transactions": self.pending_transactions
        }
    
    def from_dict(self, data: Dict):
        """Load blockchain from dictionary"""
        self.node_id = data['node_id']
        self.chain = [Block.from_dict(block_dict) for block_dict in data['chain']]
        self.pending_transactions = data['pending_transactions']
    
    def get_chain_length(self) -> int:
        """Get the length of the chain"""
        return len(self.chain)
    
    def get_all_evidence(self) -> List[Dict]:
        """Get all evidence entries"""
        # Use database if available for better performance
        if self.db:
            return self.db.get_all_evidence()
        
        # Fallback to scanning blockchain
        evidence_dict = {}
        
        for block in self.chain[1:]:
            if isinstance(block.data, list):
                for transaction in block.data:
                    evidence_id = transaction.get('evidence_id')
                    if evidence_id:
                        if evidence_id not in evidence_dict:
                            evidence_dict[evidence_id] = {
                                'evidence_id': evidence_id,
                                'description': transaction.get('description', 'N/A'),
                                'type': transaction.get('evidence_type', 'N/A'),
                                'current_officer': transaction.get('officer') or transaction.get('to_officer'),
                                'created': transaction.get('timestamp'),
                                'last_action': transaction.get('action'),
                                'block_index': block.index
                            }
                        else:
                            # Update with latest transfer info
                            if transaction.get('type') == 'evidence_transfer':
                                evidence_dict[evidence_id]['current_officer'] = transaction.get('to_officer')
                                evidence_dict[evidence_id]['last_action'] = transaction.get('action')
        
        return list(evidence_dict.values())
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        if self.db:
            return self.db.get_database_stats()
        return {
            'blocks': len(self.chain),
            'evidence': len(self.get_all_evidence()),
            'transfers': 0,
            'db_size_mb': 0,
            'db_file': 'N/A (in-memory only)'
        }