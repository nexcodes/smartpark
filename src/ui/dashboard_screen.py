"""
Dashboard Screen - Main overview of parking system
Shows total slots, occupied slots, active requests
"""
import tkinter as tk
from tkinter import ttk


class DashboardScreen(tk.Frame):
    """Main dashboard displaying system overview"""
    
    def __init__(self, parent, parking_system):
        """
        Initialize dashboard screen
        
        Args:
            parent: Parent widget
            parking_system: ParkingSystem instance
        """
        super().__init__(parent)
        self.parking_system = parking_system
        self.setup_ui()
    
    def setup_ui(self):
        """Set up dashboard UI components"""
        # Title
        title = tk.Label(
            self,
            text="System Dashboard",
            font=("Arial", 20, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(self)
        stats_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Placeholder for statistics cards
        self.create_stat_card(stats_frame, "Total Slots", "0", 0, 0)
        self.create_stat_card(stats_frame, "Occupied Slots", "0", 0, 1)
        self.create_stat_card(stats_frame, "Available Slots", "0", 0, 2)
        self.create_stat_card(stats_frame, "Active Requests", "0", 1, 0)
        self.create_stat_card(stats_frame, "Completed Requests", "0", 1, 1)
        self.create_stat_card(stats_frame, "Cancelled Requests", "0", 1, 2)
        
        # Refresh button
        refresh_btn = tk.Button(
            self,
            text="Refresh Statistics",
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            command=self.refresh_stats
        )
        refresh_btn.pack(pady=20)
    
    def create_stat_card(self, parent, title, value, row, col):
        """Create a statistics card"""
        card = tk.Frame(parent, relief=tk.RAISED, borderwidth=2, bg="white")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Title
        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 12),
            bg="white",
            fg="#7f8c8d"
        )
        title_label.pack(pady=(10, 5))
        
        # Value
        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        value_label.pack(pady=(5, 10))
        
        # Store reference for updating
        setattr(self, f"{title.lower().replace(' ', '_')}_label", value_label)
    
    def refresh_stats(self):
        """Refresh dashboard statistics"""
        # TODO: Implement actual statistics retrieval from parking_system
        print("Refreshing statistics...")
