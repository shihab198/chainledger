#!/usr/bin/env python3
"""
ChainLedger Node Launcher
Run this script to start a blockchain node
"""

import sys
import time
from blockchain import Blockchain
from network import NetworkNode
from gui import ChainLedgerGUI


def start_node(node_id: str, port: int, node_name: str):
    """Start a blockchain node with GUI"""
    
    print(f"\n{'='*60}")
    print(f"ChainLedger - Blockchain Chain of Custody System")
    print(f"{'='*60}")
    print(f"Node ID: {node_id}")
    print(f"Node Name: {node_name}")
    print(f"Port: {port}")
    print(f"{'='*60}\n")
    
    # Create blockchain
    print("Initializing blockchain...")
    blockchain = Blockchain(node_id)
    print(f"✓ Blockchain initialized with genesis block")
    
    # Create network node
    print(f"Starting network node on port {port}...")
    network = NetworkNode(blockchain, host='127.0.0.1', port=port)
    network.start()
    print(f"✓ Network node started at http://127.0.0.1:{port}")
    
    # Wait for server to start
    time.sleep(1)
    
    # Start GUI
    print("Launching GUI...")
    gui = ChainLedgerGUI(f"http://127.0.0.1:{port}", node_name)
    
    print("\n" + "="*60)
    print("ChainLedger is ready!")
    print("="*60 + "\n")
    
    # Run GUI (blocking)
    gui.run()


def print_usage():
    """Print usage information"""
    print("\nUsage: python node.py [node_number]")
    print("\nAvailable nodes:")
    print("  1 - Node A (Officer 1) - Port 5000")
    print("  2 - Node B (Officer 2) - Port 5001")
    print("  3 - Node C (Supervisor) - Port 5002")
    print("\nExample: python node.py 1")
    print("\nTo connect nodes:")
    print("  1. Start all three nodes in separate terminals")
    print("  2. In each node's GUI, go to 'Network' tab")
    print("  3. Add peer URLs:")
    print("     - http://127.0.0.1:5000")
    print("     - http://127.0.0.1:5001")
    print("     - http://127.0.0.1:5002")
    print()


if __name__ == "__main__":
    # Node configurations
    nodes = {
        '1': {'id': 'node_a', 'port': 5000, 'name': 'Node A - Officer 1'},
        '2': {'id': 'node_b', 'port': 5001, 'name': 'Node B - Officer 2'},
        '3': {'id': 'node_c', 'port': 5002, 'name': 'Node C - Supervisor'}
    }
    
    if len(sys.argv) != 2 or sys.argv[1] not in nodes:
        print_usage()
        sys.exit(1)
    
    node_num = sys.argv[1]
    config = nodes[node_num]
    
    try:
        start_node(config['id'], config['port'], config['name'])
    except KeyboardInterrupt:
        print("\n\nShutting down node...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        sys.exit(1)