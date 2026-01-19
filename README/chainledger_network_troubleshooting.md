# ChainLedger Network Connection Troubleshooting Guide

## 🔧 Common Network Connection Issues & Solutions

### Issue 1: "Failed to connect to peer" in Web Version

#### Symptoms:
- Click "Connect to Peer" but nothing happens
- Peer doesn't appear in peer list
- Error message "Failed to connect to peer"

#### Solutions:

**Solution 1: Check if peer node is actually running**

```bash
# Test if the peer is accessible
curl http://127.0.0.1:5001/api/node/info

# Or open in browser
http://127.0.0.1:5001/api/node/info
```

If this works, you should see JSON response like:
```json
{
  "node_id": "node_b",
  "node_name": "Node B - Officer 2",
  "port": 5001,
  "chain_length": 1
}
```

**Solution 2: Check browser console for errors**

1. Press `F12` to open browser developer tools
2. Go to "Console" tab
3. Try connecting again
4. Look for error messages

**Solution 3: Verify correct URL format**

✅ **Correct:**
- `http://127.0.0.1:5000`
- `http://127.0.0.1:5001`
- `http://192.168.1.100:5000`

❌ **Incorrect:**
- `127.0.0.1:5000` (missing http://)
- `http://localhost:5000/` (trailing slash - now handled)
- `https://127.0.0.1:5000` (wrong protocol)

**Solution 4: Check CORS issues**

If you see CORS errors in console, ensure Flask-CORS is installed:

```bash
pip install flask-cors
```

The web app already has CORS enabled, but verify it's in requirements.txt.

**Solution 5: Test API endpoint manually**

Open a new browser tab and navigate to:
```
http://127.0.0.1:5001/api/peers
```

You should see:
```json
{
  "peers": [],
  "count": 0
}
```

### Issue 2: Nodes Connect but Don't Sync Data

#### Symptoms:
- Peers show as "Connected" 
- Add evidence on Node A
- Evidence doesn't appear on Node B

#### Solutions:

**Solution 1: Manual sync**

1. Go to Network tab
2. Click "🔄 Sync Chain" button
3. Check if data appears

**Solution 2: Verify broadcast is working**

Check terminal/console output when adding evidence:

```
INFO:root:Broadcasted transaction to http://127.0.0.1:5001
INFO:root:Broadcasted transaction to http://127.0.0.1:5002
```

If you don't see these messages, broadcasting isn't working.

**Solution 3: Check if nodes are truly connected**

In each node:
1. Go to Network tab
2. Click "Refresh Peers"
3. Verify all peers are listed

**Solution 4: Restart nodes and reconnect**

```bash
# Stop all nodes (Ctrl+C in each terminal)

# Restart them
python app.py 1
python app.py 2
python app.py 3

# Reconnect in browser
```

### Issue 3: "Connection Refused" Error

#### Symptoms:
- Error: "Connection refused"
- Can't reach peer even though it's running

#### Solutions:

**Solution 1: Check if port is actually listening**

```bash
# Windows
netstat -an | findstr :5000

# Linux/Mac
lsof -i :5000
netstat -an | grep 5000
```

Should show:
```
TCP    0.0.0.0:5000    0.0.0.0:0    LISTENING
```

**Solution 2: Ensure Flask is binding to 0.0.0.0**

In `app.py`, verify:
```python
def run(self):
    self.app.run(host='0.0.0.0', port=self.port, debug=False)
```

NOT:
```python
self.app.run(host='127.0.0.1', ...)  # This only allows local connections
```

**Solution 3: Check firewall**

```bash
# Windows - Add firewall rule
netsh advfirewall firewall add rule name="ChainLedger" dir=in action=allow protocol=TCP localport=5000-5005

# Linux
sudo ufw allow 5000:5005/tcp

# Mac
# System Preferences → Security & Privacy → Firewall → Options
```

### Issue 4: Localhost vs IP Address Issues

#### Symptoms:
- Works with 127.0.0.1 but not with actual IP
- Or vice versa

#### Solutions:

**Solution 1: Be consistent**

If running on **same computer**, always use:
- `http://127.0.0.1:5000`
- `http://127.0.0.1:5001`
- `http://127.0.0.1:5002`

If running on **different computers**, always use actual IPs:
- `http://192.168.1.100:5000`
- `http://192.168.1.101:5000`
- `http://192.168.1.102:5000`

**Solution 2: Don't mix localhost and IP**

❌ Don't do this:
- Node A connects to: `http://localhost:5001`
- Node B connects to: `http://192.168.1.100:5000`

✅ Do this:
- All nodes use: `http://127.0.0.1:XXXX`
- OR all nodes use: `http://192.168.1.XXX:5000`

### Issue 5: Peers List Shows Duplicates

#### Symptoms:
- Same peer appears multiple times
- Peer list keeps growing

#### Solutions:

**Solution 1: Clear and reconnect**

This is a known issue. To fix:

1. Restart the node
2. Reconnect peers fresh
3. Avoid clicking "Connect" multiple times

**Solution 2: Update code to prevent duplicates**

The updated `app.py` now checks for duplicates before adding.

### Issue 6: Cross-Origin (CORS) Errors

#### Symptoms:
- Browser console shows: "CORS policy blocked"
- "Access-Control-Allow-Origin" errors

#### Solutions:

**Solution 1: Verify Flask-CORS is installed**

```bash
pip install flask-cors
```

**Solution 2: Check CORS is enabled in app.py**

```python
from flask_cors import CORS

self.app = Flask(__name__)
CORS(self.app)  # This should be present
```

**Solution 3: For production, configure CORS properly**

```python
CORS(self.app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5000", "http://127.0.0.1:5001"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

## 🧪 Testing Connection Step-by-Step

### Test 1: Can you access the node?

Open browser: `http://127.0.0.1:5000`

**Expected:** ChainLedger web interface appears  
**If fails:** Node isn't running or port is wrong

### Test 2: Can you access API?

Open browser: `http://127.0.0.1:5000/api/node/info`

**Expected:** JSON with node info  
**If fails:** API routes not working

### Test 3: Can you see peers list?

Open browser: `http://127.0.0.1:5000/api/peers`

**Expected:** JSON with peers array  
**If fails:** Peers endpoint not working

### Test 4: Can you add a peer?

Use curl or Postman:

```bash
curl -X POST http://127.0.0.1:5000/api/peers \
  -H "Content-Type: application/json" \
  -d '{"peer_url": "http://127.0.0.1:5001"}'
```

**Expected:** Success response  
**If fails:** Check request format and endpoint

### Test 5: Can nodes communicate?

```bash
# From Node A, try to reach Node B
curl http://127.0.0.1:5001/api/node/info
```

**Expected:** Node B's info  
**If fails:** Network connectivity issue

## 🔍 Debug Mode

### Enable Detailed Logging

Add to `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show all HTTP requests and responses in terminal.

### Check Network Traffic

**In Browser:**
1. Press F12
2. Go to "Network" tab
3. Try connecting to peer
4. Watch requests and responses

Look for:
- Status codes (200 = success, 404 = not found, 500 = server error)
- Request/response payloads
- Timing information

## 🛠️ Quick Fixes Checklist

When nodes won't connect, try these in order:

- [ ] Verify all nodes are actually running
- [ ] Check URLs are formatted correctly (http://)
- [ ] Ensure ports are correct (5000, 5001, 5002)
- [ ] Test API endpoint manually in browser
- [ ] Check browser console for errors (F12)
- [ ] Verify firewall isn't blocking
- [ ] Try manual sync button
- [ ] Restart nodes and reconnect
- [ ] Check terminal output for errors
- [ ] Verify Flask-CORS is installed

## 💡 Best Practices

### 1. Start Simple
Start with 2 nodes first, get them connected, then add the third.

### 2. Test Locally First
Get everything working on localhost before trying different computers.

### 3. Use Consistent URLs
Pick 127.0.0.1 OR actual IPs, don't mix.

### 4. Check Logs
Always check terminal output for error messages.

### 5. Test Connectivity
Use curl or browser to test APIs before trying GUI.

## 🐛 Still Not Working?

### Create Minimal Test

Create `test_connection.py`:

```python
import requests

# Test if peer is accessible
try:
    response = requests.get('http://127.0.0.1:5001/api/node/info', timeout=5)
    print(f"✓ Success! Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"✗ Failed: {str(e)}")

# Test adding peer
try:
    response = requests.post(
        'http://127.0.0.1:5000/api/peers',
        json={'peer_url': 'http://127.0.0.1:5001'},
        timeout=5
    )
    print(f"✓ Add peer success! Response: {response.json()}")
except Exception as e:
    print(f"✗ Add peer failed: {str(e)}")
```

Run it:
```bash
python test_connection.py
```

### Check Python Package Versions

```bash
pip list | grep -i flask
pip list | grep -i requests
```

Ensure:
- Flask >= 3.0.0
- flask-cors >= 4.0.0
- requests >= 2.31.0

### Reinstall Dependencies

```bash
pip uninstall flask flask-cors requests -y
pip install -r requirements.txt
```

## 📞 Common Error Messages Explained

| Error | Meaning | Solution |
|-------|---------|----------|
| "Connection refused" | Port not open/listening | Check if node is running |
| "CORS policy blocked" | Cross-origin issue | Install flask-cors |
| "Failed to fetch" | Network unreachable | Check URL and firewall |
| "404 Not Found" | Wrong endpoint | Verify URL path |
| "500 Internal Server Error" | Server-side crash | Check terminal logs |
| "Timeout" | Slow/no response | Check network speed |

## 🎯 Expected Behavior

When working correctly:

1. **Adding Peer:**
   - Click "Connect to Peer"
   - See success message
   - Peer appears in peer list

2. **Syncing Data:**
   - Add evidence on Node A
   - Within seconds, appears on Node B and C
   - All nodes show same chain length

3. **Network Status:**
   - Peer list shows all connected nodes
   - No duplicate entries
   - Can refresh and see updates

## ✅ Success Indicators

You'll know it's working when:

- ✓ Peers appear in peer list
- ✓ Evidence added on one node appears on others
- ✓ Chain length matches across all nodes
- ✓ No errors in browser console
- ✓ No errors in terminal output
- ✓ Blockchain validation passes on all nodes

---

**Remember:** Network issues are usually simple - check URLs, ports, and that nodes are actually running! 🚀