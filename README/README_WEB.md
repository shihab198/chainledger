# ChainLedger - Web-Based Blockchain Chain of Custody System

## 🌐 Complete Web Application

A modern, browser-based blockchain system for secure chain of custody management. Access through any web browser - no desktop application needed!

## ✨ Features

- **Beautiful Web Interface**: Modern, responsive design that works on any device
- **Real-Time Updates**: Automatic refresh and synchronization
- **Multi-Node Network**: Run distributed blockchain across multiple browsers/computers
- **Complete Blockchain Features**: Evidence management, transfers, validation, and exploration
- **Easy Access**: Just open your browser - works on desktop, tablet, and mobile

## 📁 File Structure

```
chainledger/
├── blockchain.py          # Core blockchain logic
├── network.py            # Network layer (reused from desktop version)
├── app.py                # Web application server
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── README_WEB.md         # This file
└── README.md            # Desktop version documentation
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Three Nodes

Open **three separate terminal windows**:

**Terminal 1 - Node A (Port 5000):**
```bash
python app.py 1
```

**Terminal 2 - Node B (Port 5001):**
```bash
python app.py 2
```

**Terminal 3 - Node C (Port 5002):**
```bash
python app.py 3
```

### 3. Open in Browser

After starting the nodes, open these URLs in your browser:

- **Node A**: http://127.0.0.1:5000
- **Node B**: http://127.0.0.1:5001
- **Node C**: http://127.0.0.1:5002

You can open all three in different browser tabs!

### 4. Connect the Nodes

In each browser tab:

1. Click on the **"🌐 Network"** tab
2. Use the "Quick Connect" buttons to add peers
3. Or manually enter peer URLs and click "➕ Connect to Peer"
4. Click "🔄 Refresh Peers" to see connections

## 📖 Usage Guide

### Setting Your Identity

1. Enter your name in the "Officer Name" field at the top
2. Click "Set Officer"
3. You'll see "Logged in as: [Your Name]" in green

### Adding Evidence

1. Go to **"📦 Evidence"** tab
2. Fill in the form:
   - Evidence ID (e.g., "EV-2024-001")
   - Description
   - Type (dropdown)
   - Location
3. Click "➕ Add Evidence to Blockchain"
4. Evidence appears in all connected nodes!

### Transferring Evidence

1. Go to **"🔄 Transfer"** tab
2. Fill in transfer details:
   - Evidence ID
   - From Officer (auto-filled)
   - To Officer
   - Reason for transfer
3. Click "🔀 Transfer Evidence"
4. Transfer is recorded immutably

### Viewing History

1. In the **"🔄 Transfer"** tab
2. Enter an Evidence ID
3. Click "📋 View History"
4. See complete audit trail

### Blockchain Explorer

1. Go to **"⛓️ Blockchain"** tab
2. See real-time stats (blocks, evidence count, validity)
3. Click "🔄 Refresh Blocks" to view all blocks
4. Click "✓ Validate Chain" to check integrity

### Network Management

1. Go to **"🌐 Network"** tab
2. Connect to other nodes using Quick Connect buttons
3. Click "🔄 Sync Chain" to synchronize
4. View all connected peers

## 🎨 Interface Features

### Beautiful Dashboard
- Gradient backgrounds
- Smooth animations
- Responsive design
- Real-time status indicators

### Smart Forms
- Auto-fill from logged-in officer
- Validation before submission
- Success/error alerts
- Clear feedback

### Live Updates
- Evidence list refreshes automatically
- Connection status monitoring
- Real-time chain statistics
- Automatic synchronization

## 🔧 Technical Details

### API Endpoints

All nodes expose these REST APIs:

- `GET /` - Web interface
- `GET /api/node/info` - Node information
- `GET /api/evidence` - List all evidence
- `POST /api/evidence` - Add new evidence
- `POST /api/transfer` - Transfer evidence
- `GET /api/evidence/<id>/history` - Evidence history
- `GET /api/blocks` - All blockchain blocks
- `GET /api/validate` - Validate chain
- `GET /api/peers` - List peers
- `POST /api/peers` - Add peer
- `POST /api/sync` - Sync blockchain

### Technology Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Blockchain**: Custom Python implementation
- **Communication**: REST API, JSON
- **Security**: SHA-256 hashing

## 🌍 Running on Different Computers

To run nodes on separate computers:

1. **Update app.py** - Change `'0.0.0.0'` to bind to all interfaces
2. **Note IP addresses** of each computer
3. **Update firewall** rules to allow ports 5000-5002
4. **Connect using IP addresses**: `http://192.168.1.100:5000`

Example for different computers:
- Computer A: http://192.168.1.100:5000
- Computer B: http://192.168.1.101:5001
- Computer C: http://192.168.1.102:5002

## 📱 Mobile Access

The web interface is responsive! Access from:
- Desktop computers
- Laptops
- Tablets
- Smartphones

Just open the URL in any modern browser.

## 🎯 Demo Scenarios

### Scenario 1: Complete Evidence Lifecycle

1. Open Node A in browser
2. Set officer name: "Officer Smith"
3. Add evidence: "EV-001" - "Laptop seized from suspect"
4. Open Node B in another tab
5. See evidence automatically appears
6. Transfer evidence to "Officer Johnson"
7. Check history - see complete chain

### Scenario 2: Multi-Officer Collaboration

1. Start all three nodes
2. Node A (Officer Smith) adds evidence
3. Node B (Officer Johnson) transfers to forensics
4. Node C (Supervisor) validates chain
5. All actions visible to everyone
6. Complete transparency

### Scenario 3: Network Resilience

1. Start Node A and Node B
2. Add evidence on Node A
3. Start Node C later
4. Node C syncs automatically
5. All data is consistent

## 🔒 Security Features

- **Immutable Records**: Can't change past entries
- **Cryptographic Hashing**: SHA-256 verification
- **Distributed Consensus**: Multiple nodes agree
- **Audit Trail**: Every action logged
- **Tamper Detection**: Instant validation

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Can't Connect to Peers

1. Verify all nodes are running
2. Check firewall settings
3. Use correct URLs
4. Check terminal for errors

### Browser Compatibility

Tested on:
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

## ⚡ Performance

- Fast page loads
- Instant updates
- Minimal bandwidth usage
- Smooth animations
- Efficient polling

## 🎓 Educational Value

Perfect for:
- University projects
- Blockchain demonstrations
- Forensics training
- Security workshops
- Portfolio showcase

## 📊 Statistics Dashboard

Real-time metrics:
- Number of blocks
- Total evidence count
- Chain validity status
- Connected peers
- Network health

## 🚀 Advanced Features

### Auto-Refresh
- Evidence list updates every 10 seconds
- Status indicators update every 5 seconds
- Real-time synchronization

### Visual Feedback
- Success/error alerts
- Loading indicators
- Status badges
- Color-coded states

### Smart Defaults
- Auto-fill officer names
- Quick connect buttons
- Form validation
- Responsive layouts

## 💡 Tips for Best Experience

1. **Use Chrome or Edge** for best compatibility
2. **Open in separate tabs** to see real-time sync
3. **Set officer name first** before adding evidence
4. **Connect all nodes** for full distributed experience
5. **Check validation** regularly to ensure integrity

## 🎨 Customization

Easy to customize:
- Colors and themes in HTML/CSS
- Port numbers in app.py
- Node names and IDs
- UI layout and components

## 📝 Logging

Each node logs:
- All transactions
- Network connections
- API requests
- Errors and warnings

Check terminal output for details.

## 🔄 Updates

To update the blockchain:
- Pull latest code
- Restart nodes
- Data persists in memory
- Re-sync if needed

## 🎯 Use Cases

- **Law Enforcement**: Physical evidence tracking
- **Digital Forensics**: Digital evidence management
- **Corporate Security**: Incident investigation
- **Legal**: Court admissible records
- **Training**: Educational demonstrations

## 🏆 Advantages Over Desktop Version

- ✅ No installation needed
- ✅ Cross-platform (any OS)
- ✅ Mobile friendly
- ✅ Easy to share
- ✅ Modern interface
- ✅ Faster deployment
- ✅ Better accessibility

## 📞 Support

For issues:
1. Check browser console (F12)
2. Review terminal logs
3. Verify all dependencies installed
4. Ensure ports are available
5. Test with simple scenarios first

## 🌟 Future Enhancements

Potential additions:
- User authentication
- File upload support
- Export to PDF
- Email notifications
- Advanced analytics
- Mobile app version

---

**ChainLedger Web** - Blockchain Evidence Management, Accessible Anywhere! 🔗