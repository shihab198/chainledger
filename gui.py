import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from datetime import datetime
import json
from typing import Optional


class ChainLedgerGUI:
    """Graphical User Interface for ChainLedger"""
    
    def __init__(self, node_url: str, node_name: str):
        self.node_url = node_url
        self.node_name = node_name
        self.current_officer = ""
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(f"ChainLedger - {node_name}")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Set style
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Start periodic refresh
        self.refresh_data()
    
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), 
                       background='#2c3e50', foreground='white', padding=10)
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Action.TButton', font=('Arial', 11, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = ttk.Label(
            header_frame, 
            text=f"🔗 ChainLedger - {self.node_name}",
            style='Header.TLabel'
        )
        header_label.pack(side='left', padx=20)
        
        self.status_label = ttk.Label(
            header_frame,
            text="● Connected",
            style='Header.TLabel',
            foreground='#2ecc71'
        )
        self.status_label.pack(side='right', padx=20)
        
        # Login Section
        login_frame = tk.Frame(self.root, bg='#ecf0f1', pady=10)
        login_frame.pack(fill='x')
        
        ttk.Label(login_frame, text="Officer Name:", 
                 background='#ecf0f1').pack(side='left', padx=20)
        self.officer_entry = ttk.Entry(login_frame, width=30)
        self.officer_entry.pack(side='left', padx=5)
        ttk.Button(login_frame, text="Set Officer", 
                  command=self.set_officer).pack(side='left', padx=5)
        
        self.officer_label = ttk.Label(
            login_frame, 
            text="Not logged in",
            background='#ecf0f1',
            foreground='#e74c3c',
            font=('Arial', 10, 'bold')
        )
        self.officer_label.pack(side='left', padx=20)
        
        # Main content area with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_evidence_tab()
        self.create_transfer_tab()
        self.create_blockchain_tab()
        self.create_network_tab()
    
    def create_evidence_tab(self):
        """Create evidence management tab"""
        tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(tab, text="📦 Evidence Management")
        
        # Left side - Add Evidence
        left_frame = tk.Frame(tab, bg='white', padx=20, pady=20)
        left_frame.pack(side='left', fill='both', expand=True)
        
        ttk.Label(left_frame, text="Add New Evidence", 
                 style='Title.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Evidence form
        form_frame = tk.Frame(left_frame, bg='white')
        form_frame.pack(fill='x', pady=5)
        
        ttk.Label(form_frame, text="Evidence ID:").grid(row=0, column=0, sticky='w', pady=5)
        self.evidence_id_entry = ttk.Entry(form_frame, width=40)
        self.evidence_id_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky='w', pady=5)
        self.description_entry = ttk.Entry(form_frame, width=40)
        self.description_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Type:").grid(row=2, column=0, sticky='w', pady=5)
        self.type_combo = ttk.Combobox(form_frame, width=37, state='readonly')
        self.type_combo['values'] = ('Physical', 'Digital', 'Document', 'Weapon', 
                                      'Drug', 'Electronic Device', 'Other')
        self.type_combo.current(0)
        self.type_combo.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Location:").grid(row=3, column=0, sticky='w', pady=5)
        self.location_entry = ttk.Entry(form_frame, width=40)
        self.location_entry.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Button(
            left_frame,
            text="➕ Add Evidence",
            style='Action.TButton',
            command=self.add_evidence
        ).pack(pady=20)
        
        # Right side - Evidence List
        right_frame = tk.Frame(tab, bg='white', padx=20, pady=20)
        right_frame.pack(side='right', fill='both', expand=True)
        
        ttk.Label(right_frame, text="Evidence Registry", 
                 style='Title.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Evidence treeview
        tree_frame = tk.Frame(right_frame)
        tree_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.evidence_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Description', 'Type', 'Officer', 'Action'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.evidence_tree.yview)
        
        self.evidence_tree.heading('ID', text='Evidence ID')
        self.evidence_tree.heading('Description', text='Description')
        self.evidence_tree.heading('Type', text='Type')
        self.evidence_tree.heading('Officer', text='Current Officer')
        self.evidence_tree.heading('Action', text='Last Action')
        
        self.evidence_tree.column('ID', width=120)
        self.evidence_tree.column('Description', width=200)
        self.evidence_tree.column('Type', width=100)
        self.evidence_tree.column('Officer', width=150)
        self.evidence_tree.column('Action', width=100)
        
        self.evidence_tree.pack(fill='both', expand=True)
        
        ttk.Button(
            right_frame,
            text="🔄 Refresh Evidence List",
            command=self.load_evidence_list
        ).pack(pady=10)
    
    def create_transfer_tab(self):
        """Create evidence transfer tab"""
        tab = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(tab, text="🔄 Transfer Evidence")
        
        ttk.Label(tab, text="Transfer Evidence Custody", 
                 style='Title.TLabel').pack(anchor='w', pady=(0, 20))
        
        form_frame = tk.Frame(tab, bg='white')
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Evidence ID:").grid(row=0, column=0, sticky='w', pady=10)
        self.transfer_id_entry = ttk.Entry(form_frame, width=40)
        self.transfer_id_entry.grid(row=0, column=1, pady=10, padx=10)
        
        ttk.Label(form_frame, text="From Officer:").grid(row=1, column=0, sticky='w', pady=10)
        self.from_officer_entry = ttk.Entry(form_frame, width=40)
        self.from_officer_entry.grid(row=1, column=1, pady=10, padx=10)
        
        ttk.Label(form_frame, text="To Officer:").grid(row=2, column=0, sticky='w', pady=10)
        self.to_officer_entry = ttk.Entry(form_frame, width=40)
        self.to_officer_entry.grid(row=2, column=1, pady=10, padx=10)
        
        ttk.Label(form_frame, text="Reason:").grid(row=3, column=0, sticky='w', pady=10)
        self.reason_entry = ttk.Entry(form_frame, width=40)
        self.reason_entry.grid(row=3, column=1, pady=10, padx=10)
        
        ttk.Button(
            tab,
            text="🔀 Transfer Evidence",
            style='Action.TButton',
            command=self.transfer_evidence
        ).pack(pady=20)
        
        # History section
        ttk.Label(tab, text="Evidence History", 
                 style='Title.TLabel').pack(anchor='w', pady=(20, 10))
        
        history_frame = tk.Frame(tab)
        history_frame.pack(fill='both', expand=True)
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            width=100,
            height=15,
            font=('Courier', 9)
        )
        self.history_text.pack(fill='both', expand=True)
        
        button_frame = tk.Frame(tab, bg='white')
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="📋 View History",
            command=self.view_history
        ).pack(side='left', padx=5)
    
    def create_blockchain_tab(self):
        """Create blockchain explorer tab"""
        tab = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(tab, text="⛓️ Blockchain Explorer")
        
        # Top section with info
        info_frame = tk.Frame(tab, bg='#ecf0f1', pady=10)
        info_frame.pack(fill='x', pady=(0, 10))
        
        self.chain_length_label = ttk.Label(
            info_frame,
            text="Chain Length: 0",
            background='#ecf0f1',
            font=('Arial', 11, 'bold')
        )
        self.chain_length_label.pack(side='left', padx=20)
        
        self.validity_label = ttk.Label(
            info_frame,
            text="Status: Validating...",
            background='#ecf0f1',
            font=('Arial', 11)
        )
        self.validity_label.pack(side='left', padx=20)
        
        ttk.Button(
            info_frame,
            text="✓ Validate Chain",
            command=self.validate_chain
        ).pack(side='right', padx=20)
        
        ttk.Button(
            info_frame,
            text="🔄 Refresh Blocks",
            command=self.load_blocks
        ).pack(side='right', padx=5)
        
        # Blockchain display
        self.blocks_text = scrolledtext.ScrolledText(
            tab,
            width=120,
            height=30,
            font=('Courier', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white'
        )
        self.blocks_text.pack(fill='both', expand=True)
    
    def create_network_tab(self):
        """Create network management tab"""
        tab = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        self.notebook.add(tab, text="🌐 Network")
        
        ttk.Label(tab, text="Network Peers", 
                 style='Title.TLabel').pack(anchor='w', pady=(0, 20))
        
        # Add peer section
        peer_frame = tk.Frame(tab, bg='white')
        peer_frame.pack(fill='x', pady=10)
        
        ttk.Label(peer_frame, text="Add Peer URL:").pack(side='left', padx=5)
        self.peer_url_entry = ttk.Entry(peer_frame, width=50)
        self.peer_url_entry.pack(side='left', padx=5)
        self.peer_url_entry.insert(0, "http://127.0.0.1:")
        
        ttk.Button(
            peer_frame,
            text="➕ Connect",
            command=self.add_peer
        ).pack(side='left', padx=5)
        
        ttk.Button(
            peer_frame,
            text="🔄 Sync Chain",
            command=self.sync_chain
        ).pack(side='left', padx=5)
        
        # Peers list
        self.peers_text = scrolledtext.ScrolledText(
            tab,
            width=100,
            height=20,
            font=('Courier', 10)
        )
        self.peers_text.pack(fill='both', expand=True, pady=20)
        
        ttk.Button(
            tab,
            text="🔄 Refresh Peers",
            command=self.load_peers
        ).pack()
    
    def set_officer(self):
        """Set current officer"""
        officer = self.officer_entry.get().strip()
        if officer:
            self.current_officer = officer
            self.officer_label.config(
                text=f"Logged in as: {officer}",
                foreground='#27ae60'
            )
            self.from_officer_entry.delete(0, tk.END)
            self.from_officer_entry.insert(0, officer)
            messagebox.showinfo("Success", f"Officer set to: {officer}")
        else:
            messagebox.showerror("Error", "Please enter an officer name")
    
    def add_evidence(self):
        """Add new evidence to blockchain"""
        if not self.current_officer:
            messagebox.showerror("Error", "Please set officer name first")
            return
        
        evidence_id = self.evidence_id_entry.get().strip()
        description = self.description_entry.get().strip()
        location = self.location_entry.get().strip()
        evidence_type = self.type_combo.get()
        
        if not all([evidence_id, description, location]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            response = requests.post(
                f"{self.node_url}/evidence",
                json={
                    'evidence_id': evidence_id,
                    'description': description,
                    'officer': self.current_officer,
                    'location': location,
                    'evidence_type': evidence_type
                },
                timeout=5
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Evidence added to blockchain")
                self.clear_evidence_form()
                self.load_evidence_list()
            else:
                messagebox.showerror("Error", "Failed to add evidence")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def transfer_evidence(self):
        """Transfer evidence custody"""
        evidence_id = self.transfer_id_entry.get().strip()
        from_officer = self.from_officer_entry.get().strip()
        to_officer = self.to_officer_entry.get().strip()
        reason = self.reason_entry.get().strip()
        
        if not all([evidence_id, from_officer, to_officer, reason]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            response = requests.post(
                f"{self.node_url}/transfer",
                json={
                    'evidence_id': evidence_id,
                    'from_officer': from_officer,
                    'to_officer': to_officer,
                    'reason': reason
                },
                timeout=5
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Evidence transferred")
                self.clear_transfer_form()
                self.load_evidence_list()
            else:
                messagebox.showerror("Error", "Failed to transfer evidence")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def view_history(self):
        """View evidence history"""
        evidence_id = self.transfer_id_entry.get().strip()
        if not evidence_id:
            messagebox.showerror("Error", "Please enter evidence ID")
            return
        
        try:
            response = requests.get(
                f"{self.node_url}/evidence/{evidence_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                history = data.get('history', [])
                
                self.history_text.delete(1.0, tk.END)
                self.history_text.insert(1.0, f"History for Evidence: {evidence_id}\n")
                self.history_text.insert(tk.END, "=" * 80 + "\n\n")
                
                for entry in history:
                    self.history_text.insert(tk.END, f"Block #{entry['block_index']}\n")
                    self.history_text.insert(tk.END, f"Time: {entry['timestamp']}\n")
                    self.history_text.insert(tk.END, f"Action: {entry['action']}\n")
                    self.history_text.insert(tk.END, f"Officer: {entry['officer']}\n")
                    self.history_text.insert(tk.END, "-" * 80 + "\n\n")
            else:
                messagebox.showerror("Error", "Evidence not found")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def load_evidence_list(self):
        """Load and display evidence list"""
        try:
            response = requests.get(f"{self.node_url}/evidence/all", timeout=5)
            if response.status_code == 200:
                data = response.json()
                evidence_list = data.get('evidence', [])
                
                # Clear existing items
                for item in self.evidence_tree.get_children():
                    self.evidence_tree.delete(item)
                
                # Add new items
                for evidence in evidence_list:
                    self.evidence_tree.insert('', 'end', values=(
                        evidence.get('evidence_id', 'N/A'),
                        evidence.get('description', 'N/A')[:30],
                        evidence.get('type', 'N/A'),
                        evidence.get('current_officer', 'N/A'),
                        evidence.get('last_action', 'N/A')
                    ))
        except Exception as e:
            print(f"Error loading evidence: {str(e)}")
    
    def load_blocks(self):
        """Load and display blockchain blocks"""
        try:
            response = requests.get(f"{self.node_url}/blocks", timeout=5)
            if response.status_code == 200:
                data = response.json()
                blocks = data.get('blocks', [])
                
                self.blocks_text.delete(1.0, tk.END)
                self.chain_length_label.config(text=f"Chain Length: {len(blocks)}")
                
                for block in blocks:
                    self.blocks_text.insert(tk.END, f"\n{'='*80}\n")
                    self.blocks_text.insert(tk.END, f"BLOCK #{block['index']}\n")
                    self.blocks_text.insert(tk.END, f"{'='*80}\n")
                    self.blocks_text.insert(tk.END, f"Hash: {block['hash']}\n")
                    self.blocks_text.insert(tk.END, f"Previous Hash: {block['previous_hash']}\n")
                    self.blocks_text.insert(tk.END, f"Timestamp: {datetime.fromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                    self.blocks_text.insert(tk.END, f"\nData:\n")
                    self.blocks_text.insert(tk.END, json.dumps(block['data'], indent=2) + "\n")
        except Exception as e:
            print(f"Error loading blocks: {str(e)}")
    
    def validate_chain(self):
        """Validate blockchain integrity"""
        try:
            response = requests.get(f"{self.node_url}/validate", timeout=5)
            if response.status_code == 200:
                data = response.json()
                is_valid = data.get('valid', False)
                
                if is_valid:
                    self.validity_label.config(
                        text="Status: ✓ Valid Chain",
                        foreground='#27ae60'
                    )
                    messagebox.showinfo("Validation", "Blockchain is valid!")
                else:
                    self.validity_label.config(
                        text="Status: ✗ Invalid Chain",
                        foreground='#e74c3c'
                    )
                    messagebox.showerror("Validation", "Blockchain has been tampered!")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def load_peers(self):
        """Load and display network peers"""
        try:
            response = requests.get(f"{self.node_url}/peers", timeout=5)
            if response.status_code == 200:
                data = response.json()
                peers = data.get('peers', [])
                
                self.peers_text.delete(1.0, tk.END)
                self.peers_text.insert(1.0, f"Connected Peers ({len(peers)}):\n\n")
                
                for i, peer in enumerate(peers, 1):
                    self.peers_text.insert(tk.END, f"{i}. {peer}\n")
                
                if not peers:
                    self.peers_text.insert(tk.END, "No peers connected yet.\n")
        except Exception as e:
            print(f"Error loading peers: {str(e)}")
    
    def add_peer(self):
        """Add a new peer"""
        peer_url = self.peer_url_entry.get().strip()
        if not peer_url:
            messagebox.showerror("Error", "Please enter peer URL")
            return
        
        try:
            response = requests.post(
                f"{self.node_url}/peers/add",
                json={'peer_url': peer_url},
                timeout=5
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", f"Connected to {peer_url}")
                self.load_peers()
            else:
                messagebox.showerror("Error", "Failed to connect to peer")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def sync_chain(self):
        """Synchronize blockchain with peers"""
        try:
            response = requests.post(f"{self.node_url}/sync", timeout=10)
            if response.status_code == 200:
                data = response.json()
                messagebox.showinfo("Sync", data.get('message', 'Synchronized'))
                self.load_blocks()
        except Exception as e:
            messagebox.showerror("Error", f"Sync error: {str(e)}")
    
    def clear_evidence_form(self):
        """Clear evidence form"""
        self.evidence_id_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.type_combo.current(0)
    
    def clear_transfer_form(self):
        """Clear transfer form"""
        self.transfer_id_entry.delete(0, tk.END)
        self.to_officer_entry.delete(0, tk.END)
        self.reason_entry.delete(0, tk.END)
    
    def refresh_data(self):
        """Periodically refresh data"""
        try:
            response = requests.get(f"{self.node_url}/ping", timeout=2)
            if response.status_code == 200:
                self.status_label.config(text="● Connected", foreground='#2ecc71')
            else:
                self.status_label.config(text="● Disconnected", foreground='#e74c3c')
        except:
            self.status_label.config(text="● Disconnected", foreground='#e74c3c')
        
        self.root.after(5000, self.refresh_data)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        node_url = sys.argv[1]
        node_name = sys.argv[2]
    else:
        node_url = "http://127.0.0.1:5000"
        node_name = "Node A"
    
    app = ChainLedgerGUI(node_url, node_name)
    app.run()