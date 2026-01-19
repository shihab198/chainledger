#!/usr/bin/env python3
"""
ChainLedger Network Connection Test
Test if nodes can connect to each other
"""

import requests
import sys
import time


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def test_node_running(url):
    """Test if a node is running and accessible"""
    print(f"\n🔍 Testing if node is running at {url}")
    print("-"*70)
    
    try:
        response = requests.get(f"{url}/api/node/info", timeout=3)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ SUCCESS - Node is running!")
            print(f"  Node ID: {data.get('node_id', 'Unknown')}")
            print(f"  Node Name: {data.get('node_name', 'Unknown')}")
            print(f"  Port: {data.get('port', 'Unknown')}")
            print(f"  Chain Length: {data.get('chain_length', 'Unknown')}")
            return True
        else:
            print(f"✗ FAILED - Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ FAILED - Connection refused")
        print("  → Node might not be running")
        print("  → Check if you started the node with: python app.py [1/2/3]")
        return False
    except requests.exceptions.Timeout:
        print("✗ FAILED - Connection timeout")
        print("  → Node is not responding")
        return False
    except Exception as e:
        print(f"✗ FAILED - Error: {str(e)}")
        return False


def test_peer_connection(from_url, to_url):
    """Test connecting one node to another"""
    print(f"\n🔗 Testing connection from {from_url} to {to_url}")
    print("-"*70)
    
    try:
        # First check if target node is running
        response = requests.get(f"{to_url}/api/node/info", timeout=3)
        if response.status_code != 200:
            print(f"✗ FAILED - Target node at {to_url} is not responding")
            return False
        
        # Try to add peer
        response = requests.post(
            f"{from_url}/api/peers",
            json={'peer_url': to_url},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ SUCCESS - Nodes connected!")
                print(f"  Message: {data.get('message', 'Connected')}")
                return True
            else:
                print(f"⚠ WARNING - Connection attempted but might have failed")
                print(f"  Message: {data.get('message', 'Unknown')}")
                return False
        else:
            print(f"✗ FAILED - Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ FAILED - Error: {str(e)}")
        return False


def test_peer_list(url):
    """Test getting peer list"""
    print(f"\n📋 Getting peer list from {url}")
    print("-"*70)
    
    try:
        response = requests.get(f"{url}/api/peers", timeout=3)
        if response.status_code == 200:
            data = response.json()
            peers = data.get('peers', [])
            count = data.get('count', 0)
            
            print(f"✓ SUCCESS - Retrieved peer list")
            print(f"  Peer count: {count}")
            
            if peers:
                print("  Connected peers:")
                for i, peer in enumerate(peers, 1):
                    print(f"    {i}. {peer}")
            else:
                print("  No peers connected yet")
            
            return True
        else:
            print(f"✗ FAILED - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAILED - Error: {str(e)}")
        return False


def test_sync(url):
    """Test blockchain sync"""
    print(f"\n🔄 Testing blockchain sync at {url}")
    print("-"*70)
    
    try:
        response = requests.post(f"{url}/api/sync", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ SUCCESS - Sync completed")
            print(f"  Message: {data.get('message', 'Synced')}")
            return True
        else:
            print(f"✗ FAILED - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAILED - Error: {str(e)}")
        return False


def test_add_evidence(url):
    """Test adding evidence"""
    print(f"\n📦 Testing evidence addition at {url}")
    print("-"*70)
    
    evidence_data = {
        'evidence_id': 'TEST-001',
        'description': 'Test evidence for connectivity',
        'officer': 'Test Officer',
        'location': 'Test Location',
        'evidence_type': 'Digital'
    }
    
    try:
        response = requests.post(
            f"{url}/api/evidence",
            json=evidence_data,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✓ SUCCESS - Evidence added")
            print(f"  Evidence ID: TEST-001")
            return True
        else:
            print(f"✗ FAILED - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ FAILED - Error: {str(e)}")
        return False


def test_full_network():
    """Test complete 3-node network"""
    print_header("ChainLedger Network Connection Test")
    
    nodes = {
        'Node A': 'http://127.0.0.1:5000',
        'Node B': 'http://127.0.0.1:5001',
        'Node C': 'http://127.0.0.1:5002'
    }
    
    print("\nThis test will check:")
    print("  1. If all nodes are running")
    print("  2. If nodes can connect to each other")
    print("  3. If data syncs between nodes")
    print("\nMake sure all 3 nodes are running before continuing!")
    input("\nPress Enter to start testing...")
    
    # Test 1: Check if all nodes are running
    print_header("TEST 1: Checking if nodes are running")
    
    running_nodes = {}
    for name, url in nodes.items():
        if test_node_running(url):
            running_nodes[name] = url
    
    if len(running_nodes) < 2:
        print("\n" + "="*70)
        print("⚠ WARNING: Less than 2 nodes are running!")
        print("Please start at least 2 nodes to test connectivity.")
        print("\nTo start nodes:")
        print("  Terminal 1: python app.py 1")
        print("  Terminal 2: python app.py 2")
        print("  Terminal 3: python app.py 3")
        print("="*70)
        return
    
    # Test 2: Connect nodes to each other
    print_header("TEST 2: Connecting nodes to each other")
    
    if 'Node A' in running_nodes and 'Node B' in running_nodes:
        test_peer_connection(running_nodes['Node A'], running_nodes['Node B'])
        time.sleep(1)
        test_peer_connection(running_nodes['Node B'], running_nodes['Node A'])
        time.sleep(1)
    
    if 'Node A' in running_nodes and 'Node C' in running_nodes:
        test_peer_connection(running_nodes['Node A'], running_nodes['Node C'])
        time.sleep(1)
    
    if 'Node B' in running_nodes and 'Node C' in running_nodes:
        test_peer_connection(running_nodes['Node B'], running_nodes['Node C'])
        time.sleep(1)
    
    # Test 3: Check peer lists
    print_header("TEST 3: Verifying peer lists")
    
    for name, url in running_nodes.items():
        test_peer_list(url)
    
    # Test 4: Add evidence and check sync
    print_header("TEST 4: Testing data synchronization")
    
    if 'Node A' in running_nodes:
        print("\nAdding test evidence to Node A...")
        if test_add_evidence(running_nodes['Node A']):
            print("\nWaiting 3 seconds for sync...")
            time.sleep(3)
            
            print("\nSyncing other nodes...")
            for name, url in running_nodes.items():
                if name != 'Node A':
                    test_sync(url)
    
    # Final summary
    print_header("TEST SUMMARY")
    
    print(f"\n✓ Nodes running: {len(running_nodes)}/3")
    print(f"  {', '.join(running_nodes.keys())}")
    
    print("\n📋 Next steps:")
    print("  1. Open each node in browser:")
    for name, url in running_nodes.items():
        print(f"     {name}: {url}")
    
    print("\n  2. Go to Network tab in each")
    print("  3. Click 'Refresh Peers' to see connections")
    print("  4. Go to Evidence tab to see test evidence")
    
    print("\n" + "="*70)
    print("Testing complete!")
    print("="*70 + "\n")


def interactive_test():
    """Interactive testing mode"""
    print_header("ChainLedger Network Connection Test - Interactive Mode")
    
    while True:
        print("\nSelect a test:")
        print("  1. Test if a node is running")
        print("  2. Test connection between two nodes")
        print("  3. Test peer list")
        print("  4. Test sync")
        print("  5. Test adding evidence")
        print("  6. Run full network test (3 nodes)")
        print("  7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == '1':
            url = input("Enter node URL (e.g., http://127.0.0.1:5000): ").strip()
            test_node_running(url)
        
        elif choice == '2':
            from_url = input("From URL (e.g., http://127.0.0.1:5000): ").strip()
            to_url = input("To URL (e.g., http://127.0.0.1:5001): ").strip()
            test_peer_connection(from_url, to_url)
        
        elif choice == '3':
            url = input("Enter node URL (e.g., http://127.0.0.1:5000): ").strip()
            test_peer_list(url)
        
        elif choice == '4':
            url = input("Enter node URL (e.g., http://127.0.0.1:5000): ").strip()
            test_sync(url)
        
        elif choice == '5':
            url = input("Enter node URL (e.g., http://127.0.0.1:5000): ").strip()
            test_add_evidence(url)
        
        elif choice == '6':
            test_full_network()
        
        elif choice == '7':
            print("\nExiting...\n")
            sys.exit(0)
        
        else:
            print("Invalid choice!")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        # Automatic mode - test everything
        test_full_network()
    else:
        # Interactive mode
        interactive_test()