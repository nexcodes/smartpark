"""
Analytics Screen
Displays system analytics and metrics
"""
import tkinter as tk
from tkinter import ttk


class AnalyticsScreen(tk.Frame):
    """Screen displaying analytics and metrics"""
    
    def __init__(self, parent, parking_system):
        """
        Initialize analytics screen
        
        Args:
            parent: Parent widget
            parking_system: ParkingSystem instance
        """
        super().__init__(parent)
        self.parking_system = parking_system
        self.setup_ui()
    
    def setup_ui(self):
        """Set up analytics screen UI components"""
        # Title
        title = tk.Label(
            self,
            text="System Analytics",
            font=("Arial", 20, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Control frame
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)
        
        refresh_btn = tk.Button(
            control_frame,
            text="Generate Report",
            font=("Arial", 12),
            bg="#9b59b6",
            fg="white",
            command=self.generate_report
        )
        refresh_btn.pack()
        
        # Metrics frame
        metrics_frame = tk.Frame(self)
        metrics_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # Create metrics table
        columns = ("Metric", "Value")
        self.tree = ttk.Treeview(
            metrics_frame,
            columns=columns,
            show="headings",
            height=12
        )
        
        self.tree.heading("Metric", text="Metric")
        self.tree.heading("Value", text="Value")
        self.tree.column("Metric", width=400, anchor=tk.W)
        self.tree.column("Value", width=200, anchor=tk.CENTER)
        
        # Scrollbar
        vsb = ttk.Scrollbar(
            metrics_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Layout
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Generate initial report
        self.generate_report()
    
    def generate_report(self):
        """Generate analytics report"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # TODO: Get actual analytics from parking_system
        # Placeholder metrics
        metrics = [
            ("Average Parking Duration", "N/A"),
            ("Zone A Utilization Rate", "N/A"),
            ("Zone B Utilization Rate", "N/A"),
            ("Zone C Utilization Rate", "N/A"),
            ("Total Requests", "0"),
            ("Completed Requests", "0"),
            ("Cancelled Requests", "0"),
            ("Same-Zone Allocations", "0"),
            ("Cross-Zone Allocations", "0"),
            ("Peak Usage Zone", "N/A"),
            ("Total Penalties Applied", "0"),
            ("Average Wait Time", "N/A"),
        ]
        
        for metric, value in metrics:
            self.tree.insert("", tk.END, values=(metric, value))
