#!/usr/bin/env python3
"""
ChainLedger Network Configuration Helper
Helps setup multi-computer deployments
"""

import socket
import subprocess
import platform
import sys


def get_local_ip():
    """Get the local IP address of this computer"""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unable to determine"


def get_hostname():
    """Get the hostname of this computer"""
    return socket.gethostname()


def check_port(host, port):
    """Check if a port is open on a host"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


def test_connectivity(ip):
    """Test if we can reach another computer"""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        return result.returncode == 0
    except:
        return False


def print_banner():
    """Print banner"""
    print("\n" + "="*70)
    print("ChainLedger Network Configuration Helper")
    print("="*70 + "\n")


def show_system_info():
    """Display system information"""
    print("📊 SYSTEM INFORMATION")
    print("-" * 70)
    print(f"Hostname:        {get_hostname()}")
    print(f"IP Address:      {get_local_ip()}")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version:   {sys.version.split()[0]}")
    print("-" * 70 + "\n")


def check_firewall_status():
    """Check firewall status (basic check)"""
    print("🔥 FIREWALL STATUS")
    print("-" * 70)
    
    os_type = platform.system().lower()
    
    if os_type == 'windows':
        print("Windows Firewall:")
        try:
            result = subprocess.run(
                ['netsh', 'advfirewall', 'show', 'allprofiles', 'state'],
                capture_output=True, text=True, timeout=5
            )
            if 'ON' in result.stdout:
                print("  Status: ENABLED")
                print("  ⚠️  You may need to add a firewall rule for port 5000")
                print("\n  To allow ChainLedger:")
                print('  netsh advfirewall firewall add rule name="ChainLedger" dir=in action=allow protocol=TCP localport=5000')
            else:
                print("  Status: DISABLED")
        except:
            print("  Unable to check firewall status")
    
    elif os_type == 'linux':
        print("Linux Firewall (UFW/iptables):")
        try:
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True, timeout=5)
            print(f"  {result.stdout}")
            print("\n  To allow ChainLedger:")
            print("  sudo ufw allow 5000/tcp")
        except:
            print("  UFW not found or unable to check")
    
    elif os_type == 'darwin':
        print("macOS Firewall:")
        print("  Check: System Preferences → Security & Privacy → Firewall")
        print("  Add Python/ChainLedger to allowed apps")
    
    print("-" * 70 + "\n")


def test_peer_connection():
    """Test connection to other nodes"""
    print("🔗 TEST PEER CONNECTION")
    print("-" * 70)
    
    peer_ip = input("Enter peer IP address to test (e.g., 192.168.1.100): ").strip()
    
    if not peer_ip:
        print("No IP entered, skipping test.")
        return
    
    print(f"\nTesting connection to {peer_ip}...")
    
    # Test ping
    print(f"  [1/2] Ping test...", end=" ")
    if test_connectivity(peer_ip):
        print("✓ SUCCESS")
    else:
        print("✗ FAILED - Cannot reach host")
        print("-" * 70 + "\n")
        return
    
    # Test port 5000
    print(f"  [2/2] Port 5000 test...", end=" ")
    if check_port(peer_ip, 5000):
        print("✓ SUCCESS - ChainLedger is running!")
    else:
        print("✗ FAILED - Port 5000 not accessible")
        print("\n  Possible reasons:")
        print("    • ChainLedger not running on peer")
        print("    • Firewall blocking port 5000")
        print("    • Wrong IP address")
    
    print("-" * 70 + "\n")


def generate_peer_urls():
    """Generate peer connection URLs"""
    print("🌐 GENERATE PEER URLS")
    print("-" * 70)
    
    print("Enter IP addresses of OTHER nodes (press Enter when done):\n")
    
    peers = []
    i = 1
    while True:
        ip = input(f"  Peer {i} IP address (or Enter to finish): ").strip()
        if not ip:
            break
        peers.append(f"http://{ip}:5000")
        i += 1
    
    if peers:
        print("\n✓ Peer URLs generated:")
        print("-" * 70)
        for i, peer in enumerate(peers, 1):
            print(f"  {i}. {peer}")
        print("-" * 70)
        print("\nCopy these URLs to the 'Network' tab in your ChainLedger GUI!")
    else:
        print("No peers entered.")
    
    print()


def show_quick_setup():
    """Show quick setup guide"""
    print("📋 QUICK SETUP GUIDE")
    print("="*70)
    
    my_ip = get_local_ip()
    
    print(f"""
For THIS computer ({my_ip}):
1. Share this IP with other team members: {my_ip}
2. Start ChainLedger:
   python node.py 1

For connecting to OTHER computers:
1. Get their IP addresses
2. In ChainLedger GUI → Network tab
3. Add peer URLs:
   http://[THEIR_IP]:5000
4. Click 'Connect to Peer'

Example Setup (3 computers):
┌─────────────────────────────────────────────────┐
│ Computer A (192.168.1.100) ← YOU ARE HERE      │
│   Connect to:                                   │
│   - http://192.168.1.101:5000 (Computer B)     │
│   - http://192.168.1.102:5000 (Computer C)     │
├─────────────────────────────────────────────────┤
│ Computer B (192.168.1.101)                      │
│   Connect to:                                   │
│   - http://192.168.1.100:5000 (Computer A)     │
│   - http://192.168.1.102:5000 (Computer C)     │
├─────────────────────────────────────────────────┤
│ Computer C (192.168.1.102)                      │
│   Connect to:                                   │
│   - http://192.168.1.100:5000 (Computer A)     │
│   - http://192.168.1.101:5000 (Computer B)     │
└─────────────────────────────────────────────────┘
""")
    print("="*70 + "\n")


def scan_network_nodes():
    """Scan local network for other ChainLedger nodes"""
    print("🔍 SCANNING FOR CHAINLEDGER NODES")
    print("-" * 70)
    print("Scanning local network (this may take a minute)...\n")
    
    my_ip = get_local_ip()
    if my_ip == "Unable to determine":
        print("Cannot determine local IP for scanning.")
        return
    
    # Get network prefix (e.g., 192.168.1)
    prefix = '.'.join(my_ip.split('.')[:-1])
    
    found_nodes = []
    
    # Scan common IP range
    for i in range(1, 255):
        ip = f"{prefix}.{i}"
        if ip == my_ip:
            continue
        
        # Quick port check (no output during scan)
        if check_port(ip, 5000):
            found_nodes.append(ip)
    
    if found_nodes:
        print("✓ Found ChainLedger nodes:")
        print("-" * 70)
        for i, ip in enumerate(found_nodes, 1):
            print(f"  {i}. http://{ip}:5000")
        print("-" * 70)
        print("\nCopy these URLs to connect!")
    else:
        print("No ChainLedger nodes found on local network.")
        print("\nMake sure:")
        print("  • Other nodes are running")
        print("  • All computers are on the same network")
        print("  • Firewalls allow port 5000")
    
    print()


def main():
    """Main menu"""
    print_banner()
    
    while True:
        print("Select an option:\n")
        print("  1. Show System Information")
        print("  2. Check Firewall Status")
        print("  3. Test Peer Connection")
        print("  4. Generate Peer URLs")
        print("  5. Scan Network for Nodes")
        print("  6. Show Quick Setup Guide")
        print("  7. Exit\n")
        
        choice = input("Enter your choice (1-7): ").strip()
        print()
        
        if choice == '1':
            show_system_info()
        elif choice == '2':
            check_firewall_status()
        elif choice == '3':
            test_peer_connection()
        elif choice == '4':
            generate_peer_urls()
        elif choice == '5':
            scan_network_nodes()
        elif choice == '6':
            show_quick_setup()
        elif choice == '7':
            print("Exiting...\n")
            sys.exit(0)
        else:
            print("Invalid choice!\n")
        
        input("Press Enter to continue...")
        print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...\n")
        sys.exit(0)