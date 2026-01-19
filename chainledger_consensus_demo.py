#!/usr/bin/env python3
"""
ChainLedger Consensus Demonstration
Visual demonstration of how consensus works
"""

import time
import requests
from datetime import datetime


def print_banner():
    print("\n" + "="*80)
    print("ChainLedger Consensus Mechanism Demonstration")
    print("="*80 + "\n")


def print_section(title):
    print("\n" + "-"*80)
    print(f"  {title}")
    print("-"*80)


def get_chain_info(node_url):
    """Get chain information from a node"""
    try:
        response = requests.get(f"{node_url}/api/blocks", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return {
                'url': node_url,
                'length': data['count'],
                'blocks': data['blocks']
            }
    except:
        return None


def demonstrate_consensus():
    """Demonstrate consensus mechanism step by step"""
    
    print_banner()
    
    nodes = {
        'Node A': 'http://127.0.0.1:5000',
        'Node B': 'http://127.0.0.1:5001',
        'Node C': 'http://127.0.0.1:5002'
    }
    
    print("This demonstration will show how ChainLedger's consensus works.")
    print("Make sure all 3 nodes are running and connected!\n")
    
    input("Press Enter to start...")
    
    # Step 1: Check initial state
    print_section("STEP 1: Check Initial Chain State")
    
    initial_state = {}
    for name, url in nodes.items():
        info = get_chain_info(url)
        if info:
            initial_state[name] = info
            print(f"{name}: {info['length']} blocks")
        else:
            print(f"{name}: OFFLINE or unreachable")
    
    if len(initial_state) < 2:
        print("\n⚠️  Need at least 2 nodes running!")
        return
    
    # Step 2: Create transaction on Node A
    print_section("STEP 2: Add Evidence on Node A (Transaction Creation)")
    
    print("\nCreating evidence on Node A...")
    print("This will:")
    print("  1. Create a transaction")
    print("  2. Create a block immediately (no mining)")
    print("  3. Broadcast to all connected peers")
    
    evidence_data = {
        'evidence_id': f'DEMO-{int(time.time())}',
        'description': 'Consensus demonstration evidence',
        'officer': 'Demo Officer',
        'location': 'Demo Location',
        'evidence_type': 'Digital'
    }
    
    try:
        response = requests.post(
            f"{nodes['Node A']}/api/evidence",
            json=evidence_data,
            timeout=5
        )
        if response.status_code == 200:
            print(f"\n✓ Evidence created: {evidence_data['evidence_id']}")
        else:
            print("\n✗ Failed to create evidence")
            return
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return
    
    # Step 3: Show immediate state
    print_section("STEP 3: Immediate State (Before Broadcast Completes)")
    
    time.sleep(1)  # Brief pause
    
    for name, url in nodes.items():
        info = get_chain_info(url)
        if info:
            print(f"{name}: {info['length']} blocks", end="")
            if info['length'] > initial_state.get(name, {}).get('length', 0):
                print(" ← NEW BLOCK!")
            else:
                print(" (waiting for broadcast...)")
    
    # Step 4: Wait for peer synchronization
    print_section("STEP 4: Peer Synchronization (Automatic)")
    
    print("\nWaiting for automatic synchronization (5 seconds)...")
    for i in range(5, 0, -1):
        print(f"  {i}...", end="\r")
        time.sleep(1)
    print("\n")
    
    # Step 5: Trigger manual sync
    print("Triggering manual sync on Node B and Node C...")
    for name, url in [('Node B', nodes['Node B']), ('Node C', nodes['Node C'])]:
        try:
            requests.post(f"{url}/api/sync", timeout=5)
            print(f"✓ {name} synced")
        except:
            print(f"✗ {name} sync failed")
    
    time.sleep(2)
    
    # Step 6: Verify consensus
    print_section("STEP 6: Verify Consensus Achieved")
    
    final_state = {}
    for name, url in nodes.items():
        info = get_chain_info(url)
        if info:
            final_state[name] = info
            print(f"\n{name}:")
            print(f"  Chain Length: {info['length']} blocks")
            print(f"  Latest Block Hash: {info['blocks'][-1]['hash'][:16]}...")
    
    # Check consensus
    print("\n" + "="*80)
    print("CONSENSUS CHECK:")
    print("="*80)
    
    lengths = [info['length'] for info in final_state.values()]
    hashes = [info['blocks'][-1]['hash'] for info in final_state.values()]
    
    if len(set(lengths)) == 1:
        print(f"✓ All nodes have same chain length: {lengths[0]} blocks")
    else:
        print(f"⚠️  Chain lengths differ: {lengths}")
    
    if len(set(hashes)) == 1:
        print(f"✓ All nodes have same latest block hash")
    else:
        print(f"⚠️  Latest block hashes differ")
    
    if len(set(lengths)) == 1 and len(set(hashes)) == 1:
        print("\n🎉 CONSENSUS ACHIEVED! All nodes agree on the blockchain state.")
    else:
        print("\n⚠️  Consensus not yet achieved. Try manual sync again.")
    
    # Step 7: Explain what happened
    print_section("STEP 7: What Just Happened?")
    
    print("""
1. TRANSACTION CREATION
   - User added evidence on Node A
   - Transaction created with timestamp and data

2. IMMEDIATE BLOCK CREATION (No Mining!)
   - Node A created block instantly
   - No Proof-of-Work, no mining competition
   - Block added to Node A's local chain

3. TRANSACTION BROADCAST
   - Node A sent transaction to all peers
   - Node B and Node C received transaction
   - Each peer created their own block with same transaction

4. AUTOMATIC SYNCHRONIZATION
   - Every 5 seconds, nodes auto-sync
   - Nodes compare chain lengths
   - Longest valid chain wins

5. CONSENSUS ACHIEVED
   - All nodes now have identical chains
   - Same blocks, same hashes, same data
   - Evidence visible on all nodes

KEY POINTS:
- No mining required (instant blocks)
- Longest chain wins (simple rule)
- Automatic synchronization (every 5 seconds)
- Suitable for private/trusted networks
    """)


def demonstrate_conflict():
    """Demonstrate conflict resolution"""
    
    print_section("BONUS: Conflict Resolution Demo")
    
    print("""
SCENARIO: Two nodes create blocks simultaneously

Time: 10:00:00.000
Node A: Creates Block 5 with Evidence EV-001
Node B: Creates Block 5 with Evidence EV-002

WHAT HAPPENS:
1. Both nodes have their version of block 5
2. Both broadcast to peers
3. Peers receive both transactions
4. Peers create blocks for BOTH transactions (Block 5 and 6)
5. During next sync:
   - Nodes compare chain lengths
   - Peer chain is longer (has both blocks)
   - Nodes A and B adopt peer's longer chain
6. Final state: All nodes have blocks for BOTH evidences

RESOLUTION: Longest chain wins ✓
RESULT: No data lost ✓

This is why the "Longest Chain Rule" is the consensus mechanism!
    """)


def show_consensus_properties():
    """Show consensus properties"""
    
    print_section("ChainLedger Consensus Properties")
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║                    CONSENSUS PROPERTIES                        ║
╚════════════════════════════════════════════════════════════════╝

1. MECHANISM: Longest Chain Rule
   - The chain with most blocks is considered valid
   - Similar to Bitcoin's Nakamoto Consensus
   - Simplified for private networks

2. BLOCK CREATION: Immediate (No Mining)
   - Blocks created instantly when transaction occurs
   - No Proof-of-Work computation required
   - No mining competition

3. FINALITY: Immediate (within node)
   - Block is final once created on local node
   - Network finality: ~5-10 seconds
   - No need to wait for confirmations

4. CONFLICT RESOLUTION: Automatic
   - Nodes sync periodically (every 5 seconds)
   - Longest valid chain is adopted
   - Conflicting blocks are replaced

5. FAULT TOLERANCE: N/2 - 1
   - Can tolerate up to N/2 - 1 node failures
   - Example: 3 nodes → can tolerate 1 failure
   - Requires majority of nodes to be operational

6. TRUST MODEL: Permissioned
   - Assumes nodes are trustworthy
   - Suitable for private networks
   - Not suitable for adversarial environments

╔════════════════════════════════════════════════════════════════╗
║                    COMPARISON TABLE                            ║
╚════════════════════════════════════════════════════════════════╝

Feature          | Bitcoin    | Ethereum 2.0 | ChainLedger
-----------------+------------+--------------+----------------
Mechanism        | PoW        | PoS          | Longest Chain
Block Time       | 10 min     | 12 sec       | Instant
Mining           | Yes        | No           | No
Finality         | 6 blocks   | 2 epochs     | Immediate
Energy Use       | Very High  | Low          | Minimal
Network Type     | Public     | Public       | Private
Participants     | Anyone     | Stakers      | Trusted Nodes

╔════════════════════════════════════════════════════════════════╗
║                    WHY IT WORKS                                ║
╚════════════════════════════════════════════════════════════════╝

✓ Known Participants: All nodes are authorized officers
✓ Trusted Environment: No adversarial actors
✓ Fast Operations: Evidence handling needs speed
✓ Audit Trail: Primary goal is tracking, not prevention
✓ Legal Framework: External controls prevent abuse

ChainLedger's consensus is optimized for:
- Law enforcement evidence management
- Private enterprise blockchains
- Audit and compliance systems
- Internal record keeping

NOT suitable for:
- Public cryptocurrency networks
- Adversarial environments
- High-value financial transactions
- Networks with untrusted participants
    """)


def main():
    """Main menu"""
    while True:
        print("\n" + "="*80)
        print("ChainLedger Consensus Demonstration")
        print("="*80)
        print("\nSelect an option:")
        print("  1. Run Full Consensus Demonstration")
        print("  2. Show Conflict Resolution Example")
        print("  3. Show Consensus Properties")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            demonstrate_consensus()
        elif choice == '2':
            demonstrate_conflict()
        elif choice == '3':
            show_consensus_properties()
        elif choice == '4':
            print("\nExiting...\n")
            break
        else:
            print("Invalid choice!")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...\n")