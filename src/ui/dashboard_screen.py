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
        # Background color
        self.configure(bg='#f8fafc')
        
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(self, bg='#f8fafc', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8fafc')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Make scrollable_frame expand to canvas width
        def _configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _configure_canvas)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Title section
        title_frame = tk.Frame(scrollable_frame, bg='#f8fafc')
        title_frame.pack(pady=25, padx=30, fill=tk.X)
        
        title = tk.Label(
            title_frame,
            text="📊 System Dashboard",
            font=("Segoe UI", 24, "bold"),
            fg="#1e293b",
            bg='#f8fafc'
        )
        title.pack(anchor='w')
        
        subtitle = tk.Label(
            title_frame,
            text="Real-time overview of parking system metrics",
            font=("Segoe UI", 10),
            fg="#64748b",
            bg='#f8fafc'
        )
        subtitle.pack(anchor='w', pady=(5, 0))
        
        # Stats frame with better spacing
        stats_frame = tk.Frame(scrollable_frame, bg='#f8fafc')
        stats_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        # Configure grid columns to distribute evenly
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1, uniform="col")
        
        # Statistics cards with icons and modern colors
        self.create_stat_card(stats_frame, "Total Slots", "0", 0, 0, "#3b82f6", "📦")
        self.create_stat_card(stats_frame, "Occupied Slots", "0", 0, 1, "#ef4444", "🚗")
        self.create_stat_card(stats_frame, "Available Slots", "0", 0, 2, "#22c55e", "✅")
        self.create_stat_card(stats_frame, "Active Requests", "0", 1, 0, "#f59e0b", "⏳")
        self.create_stat_card(stats_frame, "Completed Requests", "0", 1, 1, "#8b5cf6", "✓")
        self.create_stat_card(stats_frame, "Cancelled Requests", "0", 1, 2, "#64748b", "✗")
        
        # Load initial data
        self.refresh_stats()
        
        # Button frame
        button_frame = tk.Frame(scrollable_frame, bg='#f8fafc')
        button_frame.pack(pady=25, padx=30)
        
        # Refresh button with modern styling
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh Statistics",
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self.refresh_stats
        )
        refresh_btn.pack()
    
    def create_stat_card(self, parent, title, value, row, col, color="#2c3e50", icon="📊"):
        """Create a modern statistics card with icon"""
        # Card with shadow effect (using relief and borderwidth)
        card = tk.Frame(parent, relief=tk.FLAT, borderwidth=0, bg="white", highlightbackground="#e2e8f0", highlightthickness=1, height=230)
        card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        card.pack_propagate(False)
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1, minsize=250)
        parent.grid_columnconfigure(col, weight=1)
        
        # Inner padding - increased bottom padding
        inner_frame = tk.Frame(card, bg="white")
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=25)
        
        # Icon
        icon_label = tk.Label(
            inner_frame,
            text=icon,
            font=("Segoe UI", 28),
            bg="white"
        )
        icon_label.pack(pady=(0, 10))
        
        # Value (shown first, larger)
        value_label = tk.Label(
            inner_frame,
            text=value,
            font=("Segoe UI", 32, "bold"),
            bg="white",
            fg=color
        )
        value_label.pack(pady=(0, 8))
        
        # Title (shown below value) - with more padding and explicit height
        title_label = tk.Label(
            inner_frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155",
            wraplength=150,  # Wrap text if too long
            justify=tk.CENTER,
            height=2  # Fixed height to ensure visibility
        )
        title_label.pack(pady=(0, 5), anchor=tk.CENTER, fill=tk.X)
        
        # Store references for updating (both value and title for debugging)
        attr_name = f"{title.lower().replace(' ', '_')}_label"
        setattr(self, attr_name, value_label)
        # Also store title label for verification
        title_attr = f"{title.lower().replace(' ', '_')}_title_label"
        setattr(self, title_attr, title_label)
    
    def refresh_stats(self):
        """Refresh dashboard statistics from parking system"""
        try:
            # Get system statistics (correct method name is get_system_status)
            stats = self.parking_system.get_system_status()
            
            print(f"Dashboard refresh - Stats: {stats}")  # Debug
            
            # Update total slots
            self.total_slots_label.config(text=str(stats['total_slots']))
            print(f"Updated total_slots_label to: {stats['total_slots']}")  # Debug
            
            # Update occupied slots
            self.occupied_slots_label.config(text=str(stats['occupied_slots']))
            print(f"Updated occupied_slots_label to: {stats['occupied_slots']}")  # Debug
            
            # Update available slots
            self.available_slots_label.config(text=str(stats['available_slots']))
            print(f"Updated available_slots_label to: {stats['available_slots']}")  # Debug
            
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
