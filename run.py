#!/usr/bin/env python3
"""
ChainLedger Unified Launcher
Run desktop, web, or both versions simultaneously
"""

import sys
import time
import subprocess
import os


def print_banner():
    """Print application banner"""
    print("\n" + "="*70)
    print("   ____  _           _       _                    _                 ")
    print("  / ___|(_)__   __ _(_)_ __ | |    ___  ___  __ _(_)_ __   __ _    ")
    print(" | |    | '_ \\ / _` | | '_ \\| |   / _ \\/ __|/ _` | | '_ \\ / _` |   ")
    print(" | |___ | | | | (_| | | | | | |__|  __/ (__| (_| | | | | | (_| |   ")
    print("  \\____|_| |_|\\__,_|_|_| |_|_____\\___|\\___|\\__, |_|_| |_|\\__, |   ")
    print("                                            |___/         |___/    ")
    print("="*70)
    print("       Blockchain-Based Chain of Custody Management System")
    print("="*70 + "\n")


def print_menu():
    """Print main menu"""
    print("Choose how to run ChainLedger:\n")
    print("  1. Desktop GUI (Tkinter) - Single Node")
    print("  2. Web Interface (Browser) - Single Node")
    print("  3. Desktop GUI - All 3 Nodes")
    print("  4. Web Interface - All 3 Nodes")
    print("  5. Hybrid - Desktop + Web (All 6 Instances)")
    print("  6. Exit\n")


def run_desktop_node(node_num):
    """Run desktop version"""
    print(f"\nStarting Desktop Node {node_num}...")
    subprocess.Popen([sys.executable, "node.py", str(node_num)])
    time.sleep(2)


def run_web_node(node_num):
    """Run web version"""
    print(f"\nStarting Web Node {node_num}...")
    subprocess.Popen([sys.executable, "app.py", str(node_num)])
    time.sleep(2)


def run_desktop_all():
    """Run all desktop nodes"""
    print("\n" + "="*70)
    print("Starting All Desktop Nodes...")
    print("="*70)
    
    for i in range(1, 4):
        run_desktop_node(i)
    
    print("\n✓ All desktop nodes started!")
    print("\nDesktop GUIs should appear on your screen.")
    print("Ports: 5000 (Node A), 5001 (Node B), 5002 (Node C)")
    print("\nTo connect nodes:")
    print("  1. Go to Network tab in each GUI")
    print("  2. Add peers: http://127.0.0.1:5000, 5001, 5002")


def run_web_all():
    """Run all web nodes"""
    print("\n" + "="*70)
    print("Starting All Web Nodes...")
    print("="*70)
    
    for i in range(1, 4):
        run_web_node(i)
    
    print("\n✓ All web nodes started!")
    print("\nOpen these URLs in your browser:")
    print("  • Node A: http://127.0.0.1:5000")
    print("  • Node B: http://127.0.0.1:5001")
    print("  • Node C: http://127.0.0.1:5002")
    print("\nTo connect nodes:")
    print("  1. Go to Network tab in each browser window")
    print("  2. Use Quick Connect buttons or enter peer URLs")


def run_hybrid():
    """Run both desktop and web versions (6 total instances)"""
    print("\n" + "="*70)
    print("Starting HYBRID Mode - Desktop + Web (6 Instances)")
    print("="*70)
    print("\n⚠️  IMPORTANT: Hybrid mode uses separate databases")
    print("\nThis will start:")
    print("  • 3 Desktop GUI windows (ports 5000-5002)")
    print("  • 3 Web servers (ports 5003-5005)")
    print("\nDesktop nodes use: chainledger_node_a/b/c.db")
    print("Web nodes use: chainledger_web_a/b/c.db")
    print("="*70)
    
    # Start desktop nodes (ports 5000-5002)
    print("\n[1/2] Starting Desktop Nodes (ports 5000-5002)...")
    for i in range(1, 4):
        run_desktop_node(i)
    
    print("\n✓ Desktop nodes started!")
    time.sleep(2)
    
    # Start web nodes with offset ports
    print("\n[2/2] Starting Web Nodes (ports 5003-5005)...")
    
    # Create modified web node starter
    web_ports = {1: 5003, 2: 5004, 3: 5005}
    web_ids = {1: 'web_node_a', 2: 'web_node_b', 3: 'web_node_c'}
    
    for i in range(1, 4):
        port = web_ports[i]
        node_id = web_ids[i]
        node_name = f"Web Node {chr(64+i)}"
        
        # Run with custom parameters
        cmd = [
            sys.executable, "-c",
            f"from app import ChainLedgerWebApp; "
            f"app = ChainLedgerWebApp('{node_id}', {port}, '{node_name}'); "
            f"app.run()"
        ]
        subprocess.Popen(cmd)
        time.sleep(2)
    
    print("\n✓ All nodes started!")
    print("\n" + "="*70)
    print("DESKTOP NODES:")
    print("  • Node A GUI (port 5000)")
    print("  • Node B GUI (port 5001)")
    print("  • Node C GUI (port 5002)")
    print("\nWEB NODES (open in browser):")
    print("  • http://127.0.0.1:5003 (Web Node A)")
    print("  • http://127.0.0.1:5004 (Web Node B)")
    print("  • http://127.0.0.1:5005 (Web Node C)")
    print("="*70)
    print("\nNote: Desktop and Web nodes have SEPARATE blockchains.")
    print("Connect desktop nodes together, and web nodes together separately.")


def show_connection_guide():
    """Show how to connect nodes"""
    print("\n" + "="*70)
    print("NODE CONNECTION GUIDE")
    print("="*70)
    print("\nDesktop Nodes:")
    print("  1. Open 'Network' tab in each GUI window")
    print("  2. Enter peer URLs and click 'Connect':")
    print("     - http://127.0.0.1:5000")
    print("     - http://127.0.0.1:5001")
    print("     - http://127.0.0.1:5002")
    print("  3. Each node should connect to the other two")
    print("\nWeb Nodes:")
    print("  1. Open each URL in separate browser tabs")
    print("  2. Go to 'Network' tab")
    print("  3. Use 'Quick Connect' buttons or enter URLs")
    print("\nHybrid Mode:")
    print("  • Desktop nodes (5000-5002) connect to each other")
    print("  • Web nodes (5003-5005) connect to each other")
    print("  • Desktop and Web are SEPARATE networks")
    print("="*70)


def show_status():
    """Show which nodes are running"""
    print("\n" + "="*70)
    print("CHECKING RUNNING NODES...")
    print("="*70)
    
    import socket
    
    ports = {
        5000: "Node A (Desktop/Web)",
        5001: "Node B (Desktop/Web)",
        5002: "Node C (Desktop/Web)",
        5003: "Web Node A (Hybrid)",
        5004: "Web Node B (Hybrid)",
        5005: "Web Node C (Hybrid)"
    }
    
    running = []
    for port, name in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"  ✓ Port {port}: {name} - RUNNING")
            running.append(port)
        else:
            print(f"  ✗ Port {port}: {name} - NOT RUNNING")
    
    print("="*70)
    print(f"\nTotal running nodes: {len(running)}")


def main():
    """Main entry point"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            node_num = input("\nEnter node number (1-3): ").strip()
            if node_num in ['1', '2', '3']:
                run_desktop_node(node_num)
                port = 5000 + int(node_num) - 1
                print(f"\n✓ Desktop Node {node_num} started!")
                print(f"GUI should appear on your screen.")
                print(f"Port: {port}")
            else:
                print("❌ Invalid node number! Use 1, 2, or 3.")
        
        elif choice == '2':
            node_num = input("\nEnter node number (1-3): ").strip()
            if node_num in ['1', '2', '3']:
                run_web_node(node_num)
                port = 5000 + int(node_num) - 1
                print(f"\n✓ Web Node {node_num} started!")
                print(f"Open in browser: http://127.0.0.1:{port}")
            else:
                print("❌ Invalid node number! Use 1, 2, or 3.")
        
        elif choice == '3':
            run_desktop_all()
        
        elif choice == '4':
            run_web_all()
        
        elif choice == '5':
            print("\n⚠️  Hybrid mode will start 6 nodes total!")
            confirm = input("Continue? (y/n): ").strip().lower()
            if confirm == 'y':
                run_hybrid()
            else:
                print("Cancelled.")
        
        elif choice == '6':
            print("\n" + "="*70)
            print("Exiting ChainLedger Launcher...")
            print("="*70)
            print("\nTo stop running nodes:")
            print("  • Desktop: Close the GUI windows")
            print("  • Web: Press Ctrl+C in the terminal")
            print("  • Or kill processes using the ports\n")
            sys.exit(0)
        
        else:
            print("❌ Invalid choice! Please enter 1-6.")
        
        print("\n" + "-"*70)
        
        # Ask if user wants to see connection guide or status
        action = input("\nOptions: (c)onnection guide, (s)tatus, (Enter) to continue: ").strip().lower()
        if action == 'c':
            show_connection_guide()
        elif action == 's':
            show_status()
        
        input("\nPress Enter to return to menu...")
        print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("ChainLedger Launcher interrupted.")
        print("="*70)
        print("\nNodes may still be running. To stop them:")
        print("  • Close GUI windows")
        print("  • Press Ctrl+C in terminal windows")
        print("  • Or kill the Python processes\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)