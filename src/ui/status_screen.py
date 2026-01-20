"""
Allocation Status Screen
Displays current allocation status of parking requests
"""
import tkinter as tk
from tkinter import ttk


class StatusScreen(tk.Frame):
    """Screen showing allocation status"""
    
    def __init__(self, parent, parking_system):
        """
        Initialize status screen
        
        Args:
            parent: Parent widget
            parking_system: ParkingSystem instance
        """
        super().__init__(parent)
        self.parking_system = parking_system
        self.setup_ui()
    
    def setup_ui(self):
        """Set up status screen UI components"""
        # Title
        title = tk.Label(
            self,
            text="Allocation Status",
            font=("Arial", 20, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Control frame
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)
        
        refresh_btn = tk.Button(
            control_frame,
            text="Refresh",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            command=self.refresh_status
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Create treeview
        columns = ("Request ID", "Vehicle ID", "Zone", "Slot ID", "Status", "Penalty")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Load initial data
        self.refresh_status()
    
    def refresh_status(self):
        """Refresh allocation status data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # TODO: Get actual data from parking_system
        # Placeholder data
        sample_data = [
            ("1", "CAR-001", "ZONE-A", "ZONE-A-A1-1", "OCCUPIED", "0"),
            ("2", "CAR-002", "ZONE-B", "ZONE-A-A1-2", "ALLOCATED", "50"),
        ]
        
        for row in sample_data:
            self.tree.insert("", tk.END, values=row)
