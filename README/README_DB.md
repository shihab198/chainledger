# ChainLedger Database Documentation

## 📊 Database Architecture

ChainLedger now includes **persistent storage** using SQLite database. All blockchain data, evidence records, and transfers are automatically saved and persist across restarts.

## 🗄️ Database Files

Each node maintains its own database file:

```
chainledger/
├── chainledger_node_a.db     # Node A database
├── chainledger_node_b.db     # Node B database  
├── chainledger_node_c.db     # Node C database
└── database.py               # Database management code
```

### File Locations

- **Desktop Version**: Database files created in the same directory as `node.py`
- **Web Version**: Database files created in the same directory as `app.py`
- **File Naming**: `chainledger_{node_id}.db`

## 📋 Database Schema

### 1. Blocks Table

Stores the complete blockchain.

```sql
CREATE TABLE blocks (
    index_num INTEGER PRIMARY KEY,
    timestamp REAL NOT NULL,
    data TEXT NOT NULL,              -- JSON stored as text
    previous_hash TEXT NOT NULL,
    nonce INTEGER DEFAULT 0,
    hash TEXT NOT NULL,
    node_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Indexes:**
- `idx_blocks_hash` on `hash` column

### 2. Evidence Table

Quick lookup table for all evidence records.

```sql
CREATE TABLE evidence (
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
```

**Indexes:**
- `idx_evidence_officer` on `current_officer` column

### 3. Transfers Table

Complete audit trail of all evidence transfers.

```sql
CREATE TABLE transfers (
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
```

**Indexes:**
- `idx_transfers_evidence` on `evidence_id` column

### 4. Node Info Table

Tracks node metadata.

```sql
CREATE TABLE node_info (
    node_id TEXT PRIMARY KEY,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    chain_length INTEGER DEFAULT 0
)
```

## 🔄 How It Works

### Automatic Persistence

Every blockchain operation is automatically saved:

1. **Add Evidence** → Block created → Saved to database
2. **Transfer Evidence** → Block created → Saved to database
3. **Sync Chain** → New blocks → Saved to database

### Data Flow

```
User Action
    ↓
Blockchain Operation
    ↓
Block Created in Memory
    ↓
Block Saved to Database (SQLite)
    ↓
Evidence/Transfer Tables Updated
    ↓
Data Persists Forever ✓
```

### Loading on Startup

When you start a node:

1. Database file is opened (or created if new)
2. All blocks are loaded from database
3. Blockchain reconstructed in memory
4. Application continues with saved state

## 💾 Database Features

### 1. Automatic Backup

You can backup your database:

```python
from database import BlockchainDatabase

db = BlockchainDatabase("chainledger_node_a.db")
backup_path = db.backup_database()
# Creates: chainledger_backup_20241208_143022.db
```

### 2. Database Statistics

Get database information:

```python
stats = blockchain.get_database_stats()
print(stats)
# Output:
# {
#     'blocks': 42,
#     'evidence': 28,
#     'transfers': 15,
#     'db_size_mb': 0.15,
#     'db_file': 'chainledger_node_a.db'
# }
```

### 3. Fast Queries

Database provides optimized queries:

- **Get all evidence**: Direct table query (faster than scanning blockchain)
- **Get evidence history**: Indexed lookup
- **Get transfers**: Quick retrieval with foreign keys
- **Search by officer**: Indexed for performance

### 4. Data Integrity

- **Foreign keys** ensure referential integrity
- **Transactions** ensure atomic operations
- **Indexes** improve query performance
- **Unique constraints** prevent duplicates

## 🔧 Configuration Options

### Enable/Disable Database

When creating blockchain:

```python
# With database (default)
blockchain = Blockchain("node_a", use_database=True)

# Without database (in-memory only)
blockchain = Blockchain("node_a", use_database=False)
```

### Custom Database Name

```python
from database import BlockchainDatabase

# Custom database file
db = BlockchainDatabase("my_custom_blockchain.db")
```

## 📈 Performance

### Storage Efficiency

- **Lightweight**: ~150 KB per 1000 blocks
- **Compressed**: JSON data stored as text
- **Indexed**: Fast queries on large datasets
- **Scalable**: Handles thousands of evidence records

### Query Performance

| Operation | Speed | Notes |
|-----------|-------|-------|
| Get all evidence | O(n) | Direct table scan |
| Get specific evidence | O(1) | Primary key lookup |
| Get evidence history | O(log n) | Indexed search |
| Validate chain | O(n) | Must verify all blocks |

## 🛠️ Maintenance Tasks

### View Database Contents

Use any SQLite viewer:

```bash
# Command line
sqlite3 chainledger_node_a.db
.tables
SELECT * FROM evidence;
.quit

# Or use GUI tools:
# - DB Browser for SQLite
# - SQLiteStudio
# - DBeaver
```

### Backup Database

**Manual backup:**
```bash
cp chainledger_node_a.db chainledger_backup.db
```

**Programmatic backup:**
```python
blockchain.db.backup_database("backup_20241208.db")
```

### Reset/Clear Data

```python
# Clear all data (keeps schema)
blockchain.db.clear_all_data()
```

### Delete Database

```bash
# Stop the node first, then:
rm chainledger_node_a.db
```

## 🔍 Querying the Database

### Example Queries

**Get all evidence:**
```sql
SELECT * FROM evidence ORDER BY created_at DESC;
```

**Get evidence by officer:**
```sql
SELECT * FROM evidence WHERE current_officer = 'Officer Smith';
```

**Get transfer history:**
```sql
SELECT t.*, e.description 
FROM transfers t
JOIN evidence e ON t.evidence_id = e.evidence_id
WHERE t.evidence_id = 'EV-001'
ORDER BY t.timestamp;
```

**Get chain statistics:**
```sql
SELECT 
    COUNT(*) as total_blocks,
    MAX(index_num) as latest_block,
    COUNT(DISTINCT node_id) as unique_nodes
FROM blocks;
```

**Get evidence by type:**
```sql
SELECT evidence_type, COUNT(*) as count
FROM evidence
GROUP BY evidence_type;
```

## 🔐 Security Considerations

### Data Protection

1. **File Permissions**: Database files should have restricted permissions
2. **Encryption**: Consider encrypting database file at OS level
3. **Backups**: Regular backups to separate location
4. **Access Control**: Limit who can access database files

### Integrity Checks

- Blockchain validation still works (compares with in-memory chain)
- Database foreign keys ensure relational integrity
- Hash verification detects any tampering

## 🌐 Multi-Node Synchronization

### How Sync Works with Database

1. **Node A** adds evidence → Saves to `chainledger_node_a.db`
2. **Node B** syncs with Node A → Receives blocks
3. **Node B** saves blocks to `chainledger_node_b.db`
4. **Both nodes** have identical chains in their databases

### Database Independence

- Each node has its own database file
- Nodes sync via network (not database)
- Database is for persistence, not sharing
- Multiple nodes = multiple database files

## 📊 Monitoring

### Check Database Health

```python
# Get statistics
stats = blockchain.get_database_stats()
print(f"Blocks: {stats['blocks']}")
print(f"Evidence: {stats['evidence']}")
print(f"Size: {stats['db_size_mb']} MB")

# Verify chain
is_valid = blockchain.is_chain_valid()
print(f"Chain valid: {is_valid}")
```

### Database Size Growth

Approximate growth:
- **Genesis block**: ~1 KB
- **Evidence entry**: ~2 KB per block
- **Transfer**: ~1.5 KB per block
- **1000 blocks**: ~150 KB
- **10,000 blocks**: ~1.5 MB

## 🔄 Migration & Upgrades

### Exporting Data

```python
# Export all blocks as JSON
blocks = blockchain.db.get_all_blocks()
import json
with open('blockchain_export.json', 'w') as f:
    json.dump(blocks, f, indent=2)
```

### Importing Data

```python
# Import from JSON
import json
with open('blockchain_export.json', 'r') as f:
    blocks = json.load(f)

for block_dict in blocks:
    blockchain.db.save_block(block_dict, 'imported_node')
```

## 🐛 Troubleshooting

### Database Locked Error

**Cause**: Multiple processes accessing same database

**Solution**:
- Ensure only one node instance per database file
- Close all connections properly
- Check for zombie processes

### Corrupted Database

**Symptoms**: SQLite errors, crashes, invalid data

**Solution**:
```bash
# Verify database integrity
sqlite3 chainledger_node_a.db "PRAGMA integrity_check;"

# Restore from backup
cp chainledger_backup.db chainledger_node_a.db
```

### Large Database Size

**Solution**:
```sql
-- Vacuum database to reclaim space
VACUUM;

-- Analyze for query optimization
ANALYZE;
```

### Missing Data After Restart

**Cause**: Database not enabled or corrupted

**Solution**:
- Verify `use_database=True` in blockchain initialization
- Check database file exists
- Restore from backup if corrupted

## 📝 Best Practices

1. **Regular Backups**: Backup database files regularly
2. **Monitor Size**: Keep track of database growth
3. **Validate Chain**: Periodically verify blockchain integrity
4. **Clean Shutdown**: Always close applications gracefully
5. **Separate Storage**: Store backups on different drives
6. **Version Control**: Don't commit `.db` files to git
7. **Documentation**: Keep records of important evidence IDs

## 🔒 Production Considerations

For production deployment:

1. **Use PostgreSQL/MySQL** instead of SQLite for multi-user access
2. **Implement proper authentication** for database access
3. **Enable encryption** for sensitive data
4. **Set up automated backups** with retention policy
5. **Monitor performance** and optimize queries
6. **Implement audit logging** for all database operations
7. **Use connection pooling** for better performance

## 📚 API Reference

### BlockchainDatabase Class

```python
from database import BlockchainDatabase

# Initialize
db = BlockchainDatabase("chainledger.db")

# Save block
db.save_block(block_dict, node_id)

# Get blocks
blocks = db.get_all_blocks()
block = db.get_block_by_index(5)

# Evidence operations
evidence = db.get_all_evidence()
specific = db.get_evidence_by_id("EV-001")
history = db.get_evidence_history("EV-001")

# Transfers
transfers = db.get_transfers_by_evidence("EV-001")

# Stats
stats = db.get_database_stats()

# Maintenance
db.backup_database("backup.db")
db.clear_all_data()
db.close()
```

## 🎓 Educational Value

The database implementation demonstrates:

- **Persistence patterns** in blockchain
- **Relational database design** for blockchain data
- **Performance optimization** with indexes
- **Data integrity** with foreign keys
- **Transaction management** for consistency
- **Backup strategies** for critical data

## 🚀 Future Enhancements

Possible database improvements:

- [ ] Full-text search on evidence descriptions
- [ ] Advanced analytics and reporting
- [ ] Database replication for high availability
- [ ] Automatic archival of old blocks
- [ ] Blockchain pruning (keep only recent blocks)
- [ ] Multi-database support (PostgreSQL, MySQL)
- [ ] Real-time database triggers
- [ ] Encrypted database fields

---

**ChainLedger Database** - Persistent, Reliable, Secure Storage for Blockchain Evidence 🗄️