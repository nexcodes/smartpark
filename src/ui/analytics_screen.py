"""
Analytics Screen for SmartPark
Displays comprehensive analytics and statistics
"""
import tkinter as tk
from tkinter import ttk, messagebox


class AnalyticsScreen(tk.Frame):
    """Analytics screen showing system metrics and statistics"""
    
    def __init__(self, parent, parking_system):
        """
        Initialize analytics screen
        
        Args:
            parent: Parent widget (notebook)
            parking_system: ParkingSystem instance
        """
        super().__init__(parent, bg="#ecf0f1")
        self.parking_system = parking_system
        self.analytics_engine = parking_system.analytics
        
        self.setup_ui()
        self.refresh_analytics()
    
    def setup_ui(self):
        """Set up the UI components"""
        # Header
        header_frame = tk.Frame(self, bg="#34495e", height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text="📈 System Analytics & Statistics",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main content area with scrollbar
        main_frame = tk.Frame(self, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(main_frame, bg="#ecf0f1", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store reference to scrollable frame
        self.content_frame = scrollable_frame
        
        # Refresh button
        button_frame = tk.Frame(self, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh Analytics",
            command=self.refresh_analytics,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT)
        
        export_btn = tk.Button(
            button_frame,
            text="📄 Export Summary",
            command=self.export_summary,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        export_btn.pack(side=tk.LEFT, padx=(10, 0))
    
    def refresh_analytics(self):
        """Refresh all analytics data"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create sections for different analytics
        self.create_duration_section()
        self.create_request_statistics_section()
        self.create_zone_utilization_section()
        self.create_peak_zone_section()
        self.create_cross_zone_section()
    
    def create_section_card(self, title, bg_color="#ffffff"):
        """Create a card frame for a section"""
        card = tk.Frame(self.content_frame, bg=bg_color, relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, pady=10, padx=5)
        
        # Section header
        header = tk.Frame(card, bg="#2c3e50", height=40)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(
            header,
            text=title,
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=8, padx=10, anchor="w")
        
        # Content frame
        content = tk.Frame(card, bg=bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        return content
    
    def create_duration_section(self):
        """Create average parking duration section"""
        content = self.create_section_card("⏱️ Average Parking Duration")
        
        duration_data = self.analytics_engine.get_average_parking_duration()
        
        if duration_data['completed_requests'] > 0:
            # Duration display
            duration_frame = tk.Frame(content, bg="white")
            duration_frame.pack(fill=tk.X, pady=5)
            
            # Minutes
            minutes_label = tk.Label(
                duration_frame,
                text=f"{duration_data['average_duration_minutes']} min",
                font=("Arial", 32, "bold"),
                bg="white",
                fg="#3498db"
            )
            minutes_label.pack()
            
            # Seconds detail
            seconds_label = tk.Label(
                duration_frame,
                text=f"({duration_data['average_duration_seconds']} seconds)",
                font=("Arial", 11),
                bg="white",
                fg="#7f8c8d"
            )
            seconds_label.pack()
            
            # Count
            count_label = tk.Label(
                content,
                text=f"Based on {duration_data['completed_requests']} completed parking sessions",
                font=("Arial", 10),
                bg="white",
                fg="#95a5a6"
            )
            count_label.pack(pady=(10, 0))
        else:
            no_data_label = tk.Label(
                content,
                text=duration_data['message'],
                font=("Arial", 12),
                bg="white",
                fg="#e74c3c"
            )
            no_data_label.pack(pady=20)
    
    def create_request_statistics_section(self):
        """Create request statistics section"""
        content = self.create_section_card("📊 Request Statistics")
        
        request_data = self.analytics_engine.get_request_statistics()
        
        # Create grid layout for statistics
        stats_grid = tk.Frame(content, bg="white")
        stats_grid.pack(fill=tk.BOTH, expand=True)
        
        # Total requests
        self.create_stat_item(
            stats_grid,
            "Total Requests",
            str(request_data['total_requests']),
            "#3498db",
            0, 0
        )
        
        # Completed
        self.create_stat_item(
            stats_grid,
            "Completed",
            f"{request_data['completed_requests']} ({request_data['completion_rate']}%)",
            "#27ae60",
            0, 1
        )
        
        # Cancelled
        self.create_stat_item(
            stats_grid,
            "Cancelled",
            f"{request_data['cancelled_requests']} ({request_data['cancellation_rate']}%)",
            "#e74c3c",
            0, 2
        )
        
        # State breakdown
        breakdown = request_data['state_breakdown']
        self.create_stat_item(
            stats_grid,
            "Requested",
            str(breakdown['requested']),
            "#9b59b6",
            1, 0
        )
        
        self.create_stat_item(
            stats_grid,
            "Allocated",
            str(breakdown['allocated']),
            "#f39c12",
            1, 1
        )
        
        self.create_stat_item(
            stats_grid,
            "Occupied",
            str(breakdown['occupied']),
            "#16a085",
            1, 2
        )
    
    def create_stat_item(self, parent, label, value, color, row, col):
        """Create a single stat display item"""
        item_frame = tk.Frame(parent, bg="white", relief=tk.SOLID, bd=1)
        item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        parent.grid_columnconfigure(col, weight=1)
        
        value_label = tk.Label(
            item_frame,
            text=value,
            font=("Arial", 20, "bold"),
            bg="white",
            fg=color
        )
        value_label.pack(pady=(15, 5))
        
        label_label = tk.Label(
            item_frame,
            text=label,
            font=("Arial", 10),
            bg="white",
            fg="#7f8c8d"
        )
        label_label.pack(pady=(0, 15))
    
    def create_zone_utilization_section(self):
        """Create zone utilization section"""
        content = self.create_section_card("🏢 Zone Utilization")
        
        zone_data = self.analytics_engine.get_zone_utilization()
        
        if zone_data['success'] and zone_data['zones']:
            # Create table for zone utilization
            columns = ('Zone', 'Capacity', 'Occupied', 'Available', 'Utilization')
            tree = ttk.Treeview(content, columns=columns, show='headings', height=8)
            
            # Configure columns
            tree.heading('Zone', text='Zone ID')
            tree.heading('Capacity', text='Total Capacity')
            tree.heading('Occupied', text='Occupied')
            tree.heading('Available', text='Available')
            tree.heading('Utilization', text='Utilization Rate')
            
            tree.column('Zone', width=150)
            tree.column('Capacity', width=120, anchor='center')
            tree.column('Occupied', width=120, anchor='center')
            tree.column('Available', width=120, anchor='center')
            tree.column('Utilization', width=150, anchor='center')
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Insert data
            for zone in zone_data['zones']:
                tree.insert('', 'end', values=(
                    zone['zone_id'],
                    zone['total_capacity'],
                    zone['occupied'],
                    zone['available'],
                    f"{zone['utilization_rate']}%"
                ))
            
            tree.pack(side="left", fill=tk.BOTH, expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            no_data_label = tk.Label(
                content,
                text=zone_data.get('message', 'No zone data available'),
                font=("Arial", 12),
                bg="white",
                fg="#e74c3c"
            )
            no_data_label.pack(pady=20)
    
    def create_peak_zone_section(self):
        """Create peak usage zone section"""
        content = self.create_section_card("🔥 Peak Usage Zone")
        
        peak_data = self.analytics_engine.get_peak_usage_zone()
        
        if peak_data['success']:
            # Zone name
            zone_label = tk.Label(
                content,
                text=peak_data['zone_id'],
                font=("Arial", 28, "bold"),
                bg="white",
                fg="#e74c3c"
            )
            zone_label.pack(pady=(10, 5))
            
            # Utilization rate
            util_label = tk.Label(
                content,
                text=f"{peak_data['utilization_rate']}% Utilized",
                font=("Arial", 18, "bold"),
                bg="white",
                fg="#f39c12"
            )
            util_label.pack(pady=5)
            
            # Details
            details_frame = tk.Frame(content, bg="white")
            details_frame.pack(pady=10)
            
            details_text = f"Occupied: {peak_data['occupied']} | Available: {peak_data['available']} | Total: {peak_data['total_capacity']}"
            details_label = tk.Label(
                details_frame,
                text=details_text,
                font=("Arial", 11),
                bg="white",
                fg="#7f8c8d"
            )
            details_label.pack()
        else:
            no_data_label = tk.Label(
                content,
                text=peak_data['message'],
                font=("Arial", 12),
                bg="white",
                fg="#e74c3c"
            )
            no_data_label.pack(pady=20)
    
    def create_cross_zone_section(self):
        """Create cross-zone allocation statistics section"""
        content = self.create_section_card("🔄 Cross-Zone Allocation Statistics")
        
        cross_data = self.analytics_engine.get_cross_zone_allocation_statistics()
        
        # Create visual representation
        info_frame = tk.Frame(content, bg="white")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Total allocations
        total_label = tk.Label(
            info_frame,
            text=f"Total Allocations: {cross_data['total_allocated']}",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        total_label.pack(pady=(10, 15))
        
        # Same zone vs cross zone
        allocation_frame = tk.Frame(info_frame, bg="white")
        allocation_frame.pack(fill=tk.X, padx=20)
        
        # Same zone
        same_frame = tk.Frame(allocation_frame, bg="#27ae60", relief=tk.RAISED, bd=2)
        same_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
        
        same_count_label = tk.Label(
            same_frame,
            text=str(cross_data['same_zone_allocations']),
            font=("Arial", 24, "bold"),
            bg="#27ae60",
            fg="white"
        )
        same_count_label.pack(pady=(10, 5))
        
        same_label = tk.Label(
            same_frame,
            text="Same Zone",
            font=("Arial", 11),
            bg="#27ae60",
            fg="white"
        )
        same_label.pack(pady=(0, 10))
        
        # Cross zone
        cross_frame = tk.Frame(allocation_frame, bg="#e67e22", relief=tk.RAISED, bd=2)
        cross_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=5)
        
        cross_count_label = tk.Label(
            cross_frame,
            text=str(cross_data['cross_zone_allocations']),
            font=("Arial", 24, "bold"),
            bg="#e67e22",
            fg="white"
        )
        cross_count_label.pack(pady=(10, 5))
        
        cross_label = tk.Label(
            cross_frame,
            text=f"Cross Zone ({cross_data['cross_zone_percentage']}%)",
            font=("Arial", 11),
            bg="#e67e22",
            fg="white"
        )
        cross_label.pack(pady=(0, 10))
        
        # Info message
        info_label = tk.Label(
            info_frame,
            text=cross_data['message'],
            font=("Arial", 10),
            bg="white",
            fg="#7f8c8d"
        )
        info_label.pack(pady=(15, 10))
    
    def export_summary(self):
        """Export analytics summary to text"""
        try:
            summary = self.analytics_engine.display_analytics_summary()
            
            # Save to file in exports/summary/ folder
            import os
            from datetime import datetime
            
            # Create directory structure if it doesn't exist
            export_dir = os.path.join("exports", "summary")
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate filename and full path
            filename = f"analytics_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(export_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(summary)
            
            messagebox.showinfo(
                "Export Successful",
                f"Analytics summary exported to:\n{filepath}"
            )
        except Exception as e:
            messagebox.showerror(
                "Export Failed",
                f"Failed to export analytics:\n{str(e)}"
            )
    
    def on_tab_selected(self):
        """Called when this tab is selected - refresh data"""
        self.refresh_analytics()
