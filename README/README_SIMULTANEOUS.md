# Running Desktop and Web Simultaneously - Complete Guide

## 🎯 Yes, They Can Run Together!

ChainLedger supports running **both desktop and web versions simultaneously**. Here's everything you need to know.

## 🗄️ Database Separation

### The Key Understanding

Each version uses its **own separate database files**:

```
Desktop Nodes:
├── chainledger_node_a.db (port 5000)
├── chainledger_node_b.db (port 5001)
└── chainledger_node_c.db (port 5002)

Web Nodes:
├── chainledger_web_a.db  (port 5003)
├── chainledger_web_b.db  (port 5004)
└── chainledger_web_c.db  (port 5005)
```

### Why Separate Databases?

- **Prevents locking conflicts**: SQLite can't have multiple processes accessing same file
- **Independent blockchains**: Desktop and Web networks operate separately
- **Clean separation**: Different use cases, different data

## 🚀 Three Ways to Run

### Option 1: Desktop ONLY (3 Nodes)

```bash
python run.py
# Choose option 3

# Or manually:
python node.py 1  # Desktop GUI on port 5000
python node.py 2  # Desktop GUI on port 5001
python node.py 3  # Desktop GUI on port 5002
```

**Result**: 3 GUI windows, ports 5000-5002

### Option 2: Web ONLY (3 Nodes)

```bash
python run.py
# Choose option 4

# Or manually:
python app.py 1   # Web server on port 5000
python app.py 2   # Web server on port 5001
python app.py 3   # Web server on port 5002
```

**Result**: 3 web servers, open in browser

### Option 3: HYBRID MODE (6 Nodes Total!)

```bash
python run.py
# Choose option 5
```

**Result**: 
- 3 Desktop GUIs (ports 5000-5002)
- 3 Web servers (ports 5003-5005)
- **6 total nodes running!**

## 📊 Port Allocation

### Standard Mode (Desktop OR Web)

| Node | Port | Desktop | Web |
|------|------|---------|-----|
| Node A | 5000 | ✓ | ✓ |
| Node B | 5001 | ✓ | ✓ |
| Node C | 5002 | ✓ | ✓ |

### Hybrid Mode (Desktop AND Web)

| Node | Port | Type | Database |
|------|------|------|----------|
| Desktop A | 5000 | GUI | chainledger_node_a.db |
| Desktop B | 5001 | GUI | chainledger_node_b.db |
| Desktop C | 5002 | GUI | chainledger_node_c.db |
| Web A | 5003 | Browser | chainledger_web_a.db |
| Web B | 5004 | Browser | chainledger_web_b.db |
| Web C | 5005 | Browser | chainledger_web_c.db |

## 🔗 Connecting Nodes

### Connecting Desktop Nodes (to each other)

In each Desktop GUI:
1. Go to **Network** tab
2. Add peers:
   - `http://127.0.0.1:5000`
   - `http://127.0.0.1:5001`
   - `http://127.0.0.1:5002`
3. Click **Connect**
4. All desktop nodes now share data!

### Connecting Web Nodes (to each other)

In each browser tab:
1. Go to **Network** tab
2. Add peers:
   - `http://127.0.0.1:5003` (Hybrid mode)
   - `http://127.0.0.1:5004` (Hybrid mode)
   - `http://127.0.0.1:5005` (Hybrid mode)
   
   OR (Standard web mode):
   - `http://127.0.0.1:5000`
   - `http://127.0.0.1:5001`
   - `http://127.0.0.1:5002`
3. Click **Connect to Peer**
4. All web nodes now share data!

### Important: Separate Networks

❌ **Don't connect desktop to web nodes** (they're separate blockchains)

✓ **Do connect desktop nodes together**  
✓ **Do connect web nodes together**

## 🎮 Using the Unified Launcher

### Quick Start

```bash
# Install dependencies first
pip install -r requirements.txt

# Run the launcher
python run.py
```

### Launcher Menu

```
1. Desktop GUI - Single Node       → Choose node 1, 2, or 3
2. Web Interface - Single Node     → Choose node 1, 2, or 3
3. Desktop GUI - All 3 Nodes       → Starts all 3 desktop
4. Web Interface - All 3 Nodes     → Starts all 3 web
5. Hybrid - All 6 Instances        → Starts everything!
6. Exit
```

### Launcher Features

- **Connection Guide**: Press 'c' for step-by-step connection instructions
- **Status Check**: Press 's' to see which nodes are running
- **Easy Navigation**: Menu-driven interface

## 📋 Complete Setup Example

### Scenario: Run Everything

```bash
# Terminal 1: Start the launcher
python run.py

# Choose option 5 (Hybrid)
Enter your choice (1-6): 5

# Wait for all nodes to start...
```

**You'll have:**
- 3 Desktop windows appear automatically
- 3 Web servers running in background

**Then open browsers:**
- Tab 1: http://127.0.0.1:5003
- Tab 2: http://127.0.0.1:5004
- Tab 3: http://127.0.0.1:5005

**Connect Desktop nodes:**
1. In each desktop GUI → Network tab
2. Connect to: 5000, 5001, 5002

**Connect Web nodes:**
1. In each browser tab → Network tab
2. Connect to: 5003, 5004, 5005

**Now you have TWO separate blockchain networks running!**

## 🔍 Checking What's Running

### Using the Launcher

```bash
python run.py
# Choose any option
# Then press 's' for status check
```

### Manual Check

**Windows:**
```cmd
netstat -ano | findstr "5000 5001 5002 5003 5004 5005"
```

**Linux/Mac:**
```bash
lsof -i :5000-5005
```

## 🛑 Stopping Nodes

### Desktop Nodes
- Simply close the GUI windows

### Web Nodes
- Press `Ctrl+C` in the terminal

### Kill Specific Ports

**Windows:**
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

## 💡 Use Cases

### Why Run Both?

**Use Case 1: Training/Demo**
- Desktop for instructor
- Web for students
- Different data sets

**Use Case 2: Testing**
- Desktop for development
- Web for production testing
- Compare performance

**Use Case 3: Multi-Team**
- Team A uses desktop
- Team B uses web
- Independent operations

**Use Case 4: Backup**
- Primary on web
- Backup on desktop
- Redundancy

## 🎯 Best Practices

### 1. Resource Management

Running 6 nodes uses:
- **RAM**: ~300-500 MB total
- **CPU**: Minimal (idle state)
- **Disk**: ~1 MB per 1000 blocks

### 2. Port Conflicts

Always check ports before starting:
```bash
python run.py
# Press 's' to check status
```

### 3. Database Backups

Backup both sets:
```bash
# Desktop databases
cp chainledger_node_*.db backups/

# Web databases
cp chainledger_web_*.db backups/
```

### 4. Clean Shutdown

- Close desktop GUIs properly
- Use Ctrl+C for web servers
- Don't kill processes forcefully

## 📊 Performance Comparison

| Aspect | Desktop | Web |
|--------|---------|-----|
| **Speed** | Faster (native) | Fast (browser) |
| **Memory** | Lower | Slightly higher |
| **UI** | Native Tkinter | Modern HTML/CSS |
| **Access** | Local only | Network capable |
| **Mobile** | No | Yes |

## 🔧 Troubleshooting

### Problem: Port Already in Use

**Solution:**
```bash
# Check what's running
python run.py
# Press 's'

# Kill specific port
lsof -ti:5000 | xargs kill -9
```

### Problem: Database Locked

**Cause**: Same database file accessed by multiple processes

**Solution**: 
- Ensure hybrid mode is used (separate DBs)
- Or close one version before starting other

### Problem: Nodes Won't Connect

**Check:**
1. Are nodes running? (use status check)
2. Correct ports? (5000-5002 or 5003-5005)
3. Firewall blocking?
4. Using correct peer URLs?

### Problem: GUI Doesn't Appear

**Solutions:**
- Check if Tkinter installed: `python -m tkinter`
- Linux: `sudo apt-get install python3-tk`
- Try web version instead

## 🎓 Advanced Configuration

### Custom Port Ranges

Edit `run.py`:
```python
web_ports = {1: 6000, 2: 6001, 3: 6002}  # Custom ports
```

### Different Database Names

Edit `blockchain.py`:
```python
self.db = BlockchainDatabase(f"custom_{node_id}.db")
```

### Running on Different Computers

1. Desktop on Computer A
2. Web on Computer B
3. Update peer URLs with IP addresses
4. Configure firewall rules

## 📈 Scaling

### Running More Nodes

Want 10 nodes? Just modify the launcher:
```python
for i in range(1, 11):  # 10 nodes instead of 3
    run_web_node(i)
```

### Cloud Deployment

- Desktop: Not suitable (requires GUI)
- Web: Perfect for cloud (headless)
- Deploy web version on AWS/Azure/GCP

## 🎉 Quick Reference

### Start Everything
```bash
python run.py → 5 → Enter
```

### Start Just Desktop
```bash
python run.py → 3 → Enter
```

### Start Just Web
```bash
python run.py → 4 → Enter
```

### Check Status
```bash
python run.py → s → Enter
```

### See Connection Guide
```bash
python run.py → c → Enter
```

## 📝 Summary

✅ **Can run simultaneously**: Yes, with separate databases  
✅ **6 nodes total**: 3 desktop + 3 web in hybrid mode  
✅ **Independent blockchains**: Desktop and Web are separate  
✅ **Easy launcher**: `run.py` handles everything  
✅ **No conflicts**: Different ports and databases  
✅ **Production ready**: Both versions fully functional  

---

**ChainLedger** - Flexible, Powerful, Ready for Any Deployment! 🚀