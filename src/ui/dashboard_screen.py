"""
Dashboard Screen - Main overview of parking system
Shows total slots, occupied slots, active requests
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
from enums import RequestState


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
        
        # Statistics cards
        self.create_stat_card(stats_frame, "Total Slots", "0", 0, 0, "#3498db")
        self.create_stat_card(stats_frame, "Occupied Slots", "0", 0, 1, "#e74c3c")
        self.create_stat_card(stats_frame, "Available Slots", "0", 0, 2, "#27ae60")
        self.create_stat_card(stats_frame, "Active Requests", "0", 1, 0, "#f39c12")
        self.create_stat_card(stats_frame, "Completed Requests", "0", 1, 1, "#9b59b6")
        self.create_stat_card(stats_frame, "Cancelled Requests", "0", 1, 2, "#95a5a6")
        
        # Load initial data
        self.refresh_stats()
        
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
    
    def create_stat_card(self, parent, title, value, row, col, color="#2c3e50"):
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
            fg=color
        )
        value_label.pack(pady=(5, 10))
        
        # Store reference for updating
        attr_name = f"{title.lower().replace(' ', '_')}_label"
        setattr(self, attr_name, value_label)
    
    def refresh_stats(self):
        """Refresh dashboard statistics from parking system"""
        try:
            # Get system statistics (correct method name is get_system_status)
            stats = self.parking_system.get_system_status()
            
            # Update total slots
            self.total_slots_label.config(text=str(stats['total_slots']))
            
            # Update occupied slots
            self.occupied_slots_label.config(text=str(stats['occupied_slots']))
            
            # Update available slots
            self.available_slots_label.config(text=str(stats['available_slots']))
            
            # Update active requests
            self.active_requests_label.config(text=str(stats['active_requests']))
            
            # Calculate completed and cancelled requests
            completed_count = 0
            cancelled_count = 0
            
            for request in self.parking_system.requests.values():
                if request.current_state == RequestState.RELEASED:
                    completed_count += 1
                elif request.current_state == RequestState.CANCELLED:
                    cancelled_count += 1
            
            # Update completed requests
            self.completed_requests_label.config(text=str(completed_count))
            
            # Update cancelled requests
            self.cancelled_requests_label.config(text=str(cancelled_count))
            
            print("Dashboard statistics refreshed successfully")
            
        except Exception as e:
            print(f"Error refreshing statistics: {e}")
            import traceback
            traceback.print_exc()
