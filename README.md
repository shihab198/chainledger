# ChainLedger - Blockchain Chain of Custody System

A Python-based blockchain system for secure, tamper-proof chain of custody management for law enforcement, digital forensics, and cybersecurity teams.

## Features

- **Private Blockchain**: Custom-built lightweight blockchain for evidence tracking
- **Multi-Node Architecture**: Distributed system with three independent nodes
- **Tamper-Proof Records**: Cryptographic hashing ensures data integrity
- **User-Friendly GUI**: Desktop application built with Tkinter
- **Real-Time Synchronization**: Nodes communicate and sync automatically
- **Complete Audit Trail**: Track every evidence action with timestamps
- **Evidence Management**: Create, transfer, and verify evidence custody
- **Network Visualization**: Monitor connected peers and chain status

## System Requirements

- Python 3.8 or higher
- Windows, Linux, or macOS
- Network connectivity between nodes (can run on localhost for testing)

## Installation

### 1. Clone or Download the Project

Create a project directory and add all the files with this structure:

```
chainledger/
├── blockchain.py      # Core blockchain implementation
├── network.py         # Network and API layer
├── gui.py            # Graphical user interface
├── node.py           # Node launcher script
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

### 2. Install Dependencies

Open a terminal/command prompt and navigate to the project directory:

```bash
cd chainledger
pip install -r requirements.txt
```

## Quick Start Guide

### Running a Single Node (Testing)

To test the system with one node:

```bash
python node.py 1
```

This starts Node A (Officer 1) on port 5000.

### Running the Complete Network (3 Nodes)

For the full distributed experience, open **three separate terminals**:

**Terminal 1 - Node A:**
```bash
python node.py 1
```

**Terminal 2 - Node B:**
```bash
python node.py 2
```

**Terminal 3 - Node C:**
```bash
python node.py 3
```

### Connecting the Nodes

After starting all three nodes:

1. In each node's GUI, click on the **"🌐 Network"** tab
2. Add the other nodes as peers using these URLs:
   - `http://127.0.0.1:5000` (Node A)
   - `http://127.0.0.1:5001` (Node B)
   - `http://127.0.0.1:5002` (Node C)
3. Click **"➕ Connect"** for each peer
4. Verify connections by clicking **"🔄 Refresh Peers"**

## Usage Guide

### 1. Setting Your Officer Identity

Before adding evidence:
1. Enter your name in the "Officer Name" field at the top
2. Click **"Set Officer"**
3. You should see "Logged in as: [Your Name]" in green

### 2. Adding Evidence

1. Go to the **"📦 Evidence Management"** tab
2. Fill in the form:
   - **Evidence ID**: Unique identifier (e.g., "EV-2024-001")
   - **Description**: What the evidence is
   - **Type**: Select from dropdown (Physical, Digital, etc.)
   - **Location**: Where evidence was collected
3. Click **"➕ Add Evidence"**
4. The evidence is now recorded on the blockchain!

### 3. Transferring Evidence

1. Go to the **"🔄 Transfer Evidence"** tab
2. Fill in the transfer form:
   - **Evidence ID**: ID of evidence to transfer
   - **From Officer**: Current custodian (auto-filled if logged in)
   - **To Officer**: Receiving officer's name
   - **Reason**: Why evidence is being transferred
3. Click **"🔀 Transfer Evidence"**
4. The transfer is recorded immutably on the blockchain

### 4. Viewing Evidence History

1. Go to the **"🔄 Transfer Evidence"** tab
2. Enter an Evidence ID
3. Click **"📋 View History"**
4. See complete chain of custody with all actions

### 5. Blockchain Explorer

1. Go to the **"⛓️ Blockchain Explorer"** tab
2. Click **"🔄 Refresh Blocks"** to see all blocks
3. Click **"✓ Validate Chain"** to verify integrity
4. View complete blockchain with hashes and timestamps

### 6. Network Management

1. Go to the **"🌐 Network"** tab
2. Add peer nodes to create distributed network
3. Click **"🔄 Sync Chain"** to synchronize with peers
4. View all connected nodes

## Architecture Overview

### Components

1. **blockchain.py**: Core blockchain logic
   - Block creation and validation
   - SHA-256 hashing
   - Chain integrity verification
   - Evidence transaction management

2. **network.py**: Networking layer
   - Flask REST API
   - Peer-to-peer communication
   - Transaction broadcasting
   - Chain synchronization

3. **gui.py**: User interface
   - Tkinter-based desktop GUI
   - Evidence management forms
   - Blockchain visualization
   - Real-time status updates

4. **node.py**: Node launcher
   - Initializes blockchain
   - Starts network server
   - Launches GUI

### Data Flow

1. **Evidence Creation/Transfer**:
   - Officer submits action via GUI
   - Transaction created with metadata
   - Block added to local chain
   - Transaction broadcast to all peers
   - Peers validate and add to their chains

2. **Chain Synchronization**:
   - Nodes periodically check peer chain lengths
   - Longest valid chain is adopted
   - Ensures all nodes have same data

## API Endpoints

Each node exposes a REST API:

- `GET /ping` - Check node status
- `GET /chain` - Get full blockchain
- `GET /blocks` - Get all blocks
- `POST /evidence` - Add new evidence
- `POST /transfer` - Transfer evidence
- `GET /evidence/<id>` - Get evidence history
- `GET /evidence/all` - Get all evidence
- `GET /validate` - Validate chain integrity
- `GET /peers` - List connected peers
- `POST /peers/add` - Add new peer
- `POST /sync` - Synchronize chain

## Testing Scenarios

### Scenario 1: Single Evidence Lifecycle

1. Start all three nodes
2. On Node A: Add evidence "EV-001"
3. Verify evidence appears on all nodes
4. On Node B: Transfer EV-001 to another officer
5. Check history shows complete chain

### Scenario 2: Network Resilience

1. Start Node A and Node B, connect them
2. Add evidence on Node A
3. Start Node C, connect to Node A
4. Node C should sync and receive all data

### Scenario 3: Integrity Verification

1. Add several evidence entries
2. Click "Validate Chain" on any node
3. System should confirm chain is valid
4. All nodes maintain consistent state

## Security Features

- **Cryptographic Hashing**: SHA-256 hashing of all blocks
- **Immutability**: Any tampering invalidates the chain
- **Distributed Consensus**: Multiple nodes must agree
- **Audit Trail**: Complete history of all actions
- **Timestamp Verification**: All actions are timestamped

## Troubleshooting

### Port Already in Use

If you get a port error:
```bash
# Kill process using the port (replace 5000 with your port)
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

### Nodes Won't Connect

1. Ensure all nodes are running
2. Check firewall settings
3. Verify correct URLs are being used
4. Check terminal for error messages

### GUI Not Appearing

1. Ensure tkinter is installed:
   ```bash
   python -m tkinter
   ```
2. On Linux, install: `sudo apt-get install python3-tk`

## Use Cases

- **Law Enforcement**: Track physical evidence (weapons, documents, drugs)
- **Digital Forensics**: Chain of custody for disk images, logs, server data
- **Corporate Security**: Internal incident investigation management
- **Legal Proceedings**: Provide cryptographically verifiable custody records

## Advanced Configuration

### Running on Multiple Computers

1. Edit `network.py` to use actual IP addresses instead of 127.0.0.1
2. Update firewall rules to allow traffic on ports 5000-5002
3. Use actual IP addresses when connecting peers

### Customizing Port Numbers

Edit the `nodes` dictionary in `node.py`:
```python
nodes = {
    '1': {'id': 'node_a', 'port': YOUR_PORT, 'name': 'Node A'},
    ...
}
```

## Project Structure Details

```
chainledger/
│
├── blockchain.py          # 200+ lines - Core blockchain
│   ├── Block class        # Individual block structure
│   └── Blockchain class   # Chain management
│
├── network.py             # 180+ lines - Networking
│   └── NetworkNode class  # REST API and P2P
│
├── gui.py                 # 550+ lines - User interface
│   └── ChainLedgerGUI     # Full Tkinter application
│
├── node.py               # 80+ lines - Node launcher
│   └── start_node()      # Initialize and run node
│
├── requirements.txt      # Python dependencies
└── README.md            # Documentation
```

## Future Enhancements

- Digital signatures for authentication
- Encrypted evidence metadata
- QR code evidence tagging
- Mobile app interface
- Integration with evidence hashing tools
- PostgreSQL backend for production
- Multi-factor authentication
- Role-based access control (RBAC)

## License

This project is for educational and demonstration purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review terminal logs for errors
3. Ensure all dependencies are installed
4. Verify Python version is 3.8+

## Credits

Developed as a demonstration of blockchain technology applied to real-world chain of custody management for law enforcement and digital forensics.

---

**ChainLedger** - Securing Evidence Integrity Through Blockchain Technology