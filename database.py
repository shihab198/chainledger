import sqlite3
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class BlockchainDatabase:
    """SQLite database for persistent blockchain storage"""
    
    def __init__(self, db_name: str = "chainledger.db"):
        self.db_name = db_name
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Create blocks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                index_num INTEGER PRIMARY KEY,
                timestamp REAL NOT NULL,
                data TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                nonce INTEGER DEFAULT 0,
                hash TEXT NOT NULL,
                node_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create evidence table for quick lookups
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id TEXT PRIMARY KEY,
                description TEXT,
                evidence_type TEXT,
                current_officer TEXT,
                location TEXT,
                created_by TEXT,
                created_at TIMESTAMP,
                last_action TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                block_index INTEGER,
                FOREIGN KEY (block_index) REFERENCES blocks(index_num)
            )
        ''')
        
        # Create transfers table for audit trail
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evidence_id TEXT NOT NULL,
                from_officer TEXT NOT NULL,
                to_officer TEXT NOT NULL,
                reason TEXT,
                timestamp TIMESTAMP NOT NULL,
                block_index INTEGER,
                FOREIGN KEY (evidence_id) REFERENCES evidence(evidence_id),
                FOREIGN KEY (block_index) REFERENCES blocks(index_num)
            )
        ''')
        
        # Create node_info table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS node_info (
                node_id TEXT PRIMARY KEY,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                chain_length INTEGER DEFAULT 0
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_evidence_officer ON evidence(current_officer)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transfers_evidence ON transfers(evidence_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_blocks_hash ON blocks(hash)')
        
        self.conn.commit()
        print(f"✓ Database initialized: {self.db_name}")
    
    def save_block(self, block_dict: Dict, node_id: str) -> bool:
        """Save a block to the database"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO blocks 
                (index_num, timestamp, data, previous_hash, nonce, hash, node_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                block_dict['index'],
                block_dict['timestamp'],
                json.dumps(block_dict['data']),
                block_dict['previous_hash'],
                block_dict['nonce'],
                block_dict['hash'],
                node_id
            ))
            
            # Process transactions in the block
            self._process_block_transactions(block_dict)
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving block: {e}")
            self.conn.rollback()
            return False
    
    def _process_block_transactions(self, block_dict: Dict):
        """Process transactions in a block and update evidence/transfers tables"""
        cursor = self.conn.cursor()
        data = block_dict['data']
        
        # Skip genesis block
        if block_dict['index'] == 0:
            return
        
        # Process each transaction
        if isinstance(data, list):
            for transaction in data:
                trans_type = transaction.get('type')
                evidence_id = transaction.get('evidence_id')
                
                if trans_type == 'evidence_creation':
                    # Insert or update evidence
                    cursor.execute('''
                        INSERT OR REPLACE INTO evidence 
                        (evidence_id, description, evidence_type, current_officer, 
                         location, created_by, created_at, last_action, block_index)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        evidence_id,
                        transaction.get('description'),
                        transaction.get('evidence_type'),
                        transaction.get('officer'),
                        transaction.get('location'),
                        transaction.get('officer'),
                        transaction.get('timestamp'),
                        'Created',
                        block_dict['index']
                    ))
                
                elif trans_type == 'evidence_transfer':
                    # Update evidence current officer
                    cursor.execute('''
                        UPDATE evidence 
                        SET current_officer = ?, last_action = ?, last_updated = ?
                        WHERE evidence_id = ?
                    ''', (
                        transaction.get('to_officer'),
                        'Transferred',
                        transaction.get('timestamp'),
                        evidence_id
                    ))
                    
                    # Record transfer
                    cursor.execute('''
                        INSERT INTO transfers 
                        (evidence_id, from_officer, to_officer, reason, timestamp, block_index)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        evidence_id,
                        transaction.get('from_officer'),
                        transaction.get('to_officer'),
                        transaction.get('reason'),
                        transaction.get('timestamp'),
                        block_dict['index']
                    ))
    
    def get_all_blocks(self) -> List[Dict]:
        """Retrieve all blocks from database"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM blocks ORDER BY index_num')
        rows = cursor.fetchall()
        
        blocks = []
        for row in rows:
            block = {
                'index': row['index_num'],
                'timestamp': row['timestamp'],
                'data': json.loads(row['data']),
                'previous_hash': row['previous_hash'],
                'nonce': row['nonce'],
                'hash': row['hash']
            }
            blocks.append(block)
        
        return blocks
    
    def get_block_by_index(self, index: int) -> Optional[Dict]:
        """Get a specific block by index"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM blocks WHERE index_num = ?', (index,))
        row = cursor.fetchone()
        
        if row:
            return {
                'index': row['index_num'],
                'timestamp': row['timestamp'],
                'data': json.loads(row['data']),
                'previous_hash': row['previous_hash'],
                'nonce': row['nonce'],
                'hash': row['hash']
            }
        return None
    
    def get_chain_length(self) -> int:
        """Get the length of the blockchain"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM blocks')
        result = cursor.fetchone()
        return result['count'] if result else 0
    
    def get_all_evidence(self) -> List[Dict]:
        """Get all evidence from database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT evidence_id, description, evidence_type, current_officer,
                   location, created_by, created_at, last_action
            FROM evidence
            ORDER BY created_at DESC
        ''')
        rows = cursor.fetchall()
        
        evidence_list = []
        for row in rows:
            evidence_list.append({
                'evidence_id': row['evidence_id'],
                'description': row['description'],
                'type': row['evidence_type'],
                'current_officer': row['current_officer'],
                'location': row['location'],
                'created_by': row['created_by'],
                'created': row['created_at'],
                'last_action': row['last_action']
            })
        
        return evidence_list
    
    def get_evidence_by_id(self, evidence_id: str) -> Optional[Dict]:
        """Get specific evidence by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM evidence WHERE evidence_id = ?', (evidence_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'evidence_id': row['evidence_id'],
                'description': row['description'],
                'type': row['evidence_type'],
                'current_officer': row['current_officer'],
                'location': row['location'],
                'created_by': row['created_by'],
                'created': row['created_at'],
                'last_action': row['last_action']
            }
        return None
    
    def get_evidence_history(self, evidence_id: str) -> List[Dict]:
        """Get complete history of evidence from blockchain"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT b.index_num, b.timestamp, b.data
            FROM blocks b
            WHERE b.data LIKE ?
            ORDER BY b.index_num
        ''', (f'%{evidence_id}%',))
        
        rows = cursor.fetchall()
        history = []
        
        for row in rows:
            data = json.loads(row['data'])
            if isinstance(data, list):
                for transaction in data:
                    if transaction.get('evidence_id') == evidence_id:
                        history.append({
                            'block_index': row['index_num'],
                            'timestamp': transaction.get('timestamp'),
                            'action': transaction.get('action'),
                            'officer': transaction.get('officer') or transaction.get('to_officer'),
                            'details': transaction
                        })
        
        return history
    
    def get_transfers_by_evidence(self, evidence_id: str) -> List[Dict]:
        """Get all transfers for specific evidence"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM transfers 
            WHERE evidence_id = ?
            ORDER BY timestamp DESC
        ''', (evidence_id,))
        
        rows = cursor.fetchall()
        transfers = []
        
        for row in rows:
            transfers.append({
                'id': row['id'],
                'evidence_id': row['evidence_id'],
                'from_officer': row['from_officer'],
                'to_officer': row['to_officer'],
                'reason': row['reason'],
                'timestamp': row['timestamp'],
                'block_index': row['block_index']
            })
        
        return transfers
    
    def update_node_info(self, node_id: str, chain_length: int):
        """Update node information"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO node_info (node_id, last_active, chain_length)
            VALUES (?, CURRENT_TIMESTAMP, ?)
        ''', (node_id, chain_length))
        self.conn.commit()
    
    def clear_all_data(self):
        """Clear all data (for testing/reset)"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM transfers')
        cursor.execute('DELETE FROM evidence')
        cursor.execute('DELETE FROM blocks')
        cursor.execute('DELETE FROM node_info')
        self.conn.commit()
        print("✓ All data cleared from database")
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM blocks')
        blocks_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM evidence')
        evidence_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM transfers')
        transfers_count = cursor.fetchone()['count']
        
        # Get database file size
        db_size = os.path.getsize(self.db_name) if os.path.exists(self.db_name) else 0
        db_size_mb = db_size / (1024 * 1024)
        
        return {
            'blocks': blocks_count,
            'evidence': evidence_count,
            'transfers': transfers_count,
            'db_size_mb': round(db_size_mb, 2),
            'db_file': self.db_name
        }
    
    def backup_database(self, backup_path: str = None):
        """Create a backup of the database"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"chainledger_backup_{timestamp}.db"
        
        try:
            import shutil
            shutil.copy2(self.db_name, backup_path)
            print(f"✓ Database backed up to: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"Error backing up database: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()