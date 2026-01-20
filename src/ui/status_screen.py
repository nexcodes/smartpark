"""
Allocation Status Screen
Displays current allocation status of parking requests
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from enums import RequestState


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
        # Background
        self.configure(bg='#f8fafc')
        
        # Title section
        title_frame = tk.Frame(self, bg='#f8fafc')
        title_frame.pack(pady=25, padx=30, fill=tk.X)
        
        title = tk.Label(
            title_frame,
            text="📍 Allocation Status",
            font=("Segoe UI", 24, "bold"),
            fg="#1e293b",
            bg='#f8fafc'
        )
        title.pack(anchor='w')
        
        subtitle = tk.Label(
            title_frame,
            text="View and manage parking request allocations",
            font=("Segoe UI", 10),
            fg="#64748b",
            bg='#f8fafc'
        )
        subtitle.pack(anchor='w', pady=(5, 0))
        
        # Control frame with modern styling
        control_frame = tk.Frame(self, bg='white', highlightbackground="#e2e8f0", highlightthickness=1)
        control_frame.pack(pady=15, padx=30, fill=tk.X)
        
        inner_control = tk.Frame(control_frame, bg='white')
        inner_control.pack(pady=15, padx=20, fill=tk.X)
        
        # Filter options
        tk.Label(inner_control, text="Filter by Status:", font=("Segoe UI", 11, "bold"),
                bg='white', fg='#1e293b').pack(side=tk.LEFT, padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="ALL")
        filter_options = ["ALL", "REQUESTED", "ALLOCATED", "OCCUPIED", "RELEASED", "CANCELLED"]
        
        style = ttk.Style()
        style.configure('Status.TCombobox', padding=5)
        
        self.filter_combobox = ttk.Combobox(
            inner_control,
            textvariable=self.filter_var,
            values=filter_options,
            font=("Segoe UI", 10),
            width=15,
            state="readonly",
            style='Status.TCombobox'
        )
        self.filter_combobox.pack(side=tk.LEFT, padx=5)
        self.filter_combobox.bind("<<ComboboxSelected>>", lambda e: self.refresh_status())
        
        refresh_btn = tk.Button(
            inner_control,
            text="🔄 Refresh",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.refresh_status
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        # Stats label
        self.stats_label = tk.Label(
            inner_control,
            text="Total Requests: 0",
            font=("Segoe UI", 10),
            fg="#64748b",
            bg='white'
        )
        self.stats_label.pack(side=tk.LEFT, padx=20)
        
        # Action buttons frame
        action_frame = tk.Frame(self, bg='#f8fafc')
        action_frame.pack(pady=15, padx=30)
        
        tk.Label(
            action_frame,
            text="Actions on Selected Request:",
            font=("Segoe UI", 11, "bold"),
            fg="#1e293b",
            bg='#f8fafc'
        ).pack(side=tk.LEFT, padx=10)
        
        # Mark as Occupied button
        self.occupy_btn = tk.Button(
            action_frame,
            text="✅ Mark as Occupied",
            font=("Segoe UI", 10, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.mark_occupied
        )
        self.occupy_btn.pack(side=tk.LEFT, padx=5)
        
        # Release Parking button
        self.release_btn = tk.Button(
            action_frame,
            text="🚦 Release Parking",
            font=("Segoe UI", 10, "bold"),
            bg="#8b5cf6",
            fg="white",
            activebackground="#7c3aed",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.release_parking
        )
        self.release_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel Request button
        self.cancel_btn = tk.Button(
            action_frame,
            text="❌ Cancel Request",
            font=("Segoe UI", 10, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.cancel_request
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Table frame with card styling
        table_frame = tk.Frame(self, bg='white', highlightbackground="#e2e8f0", highlightthickness=1)
        table_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        # Style the treeview
        style = ttk.Style()
        style.configure('Modern.Treeview',
                       font=('Segoe UI', 10),
                       rowheight=30,
                       background='white',
                       fieldbackground='white',
                       foreground='#1e293b')
        style.configure('Modern.Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background='#f1f5f9',
                       foreground='#1e293b')
        style.map('Modern.Treeview',
                 background=[('selected', '#2563eb')],
                 foreground=[('selected', 'white')])
        
        # Create treeview with updated columns
        columns = ("Request ID", "Vehicle ID", "Requested Zone", "Allocated Zone", "Slot ID", "Status", "Penalty", "Timestamp")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15, style='Modern.Treeview')
        
        # Define headings and column widths
        column_widths = {
            "Request ID": 100,
            "Vehicle ID": 120,
            "Requested Zone": 120,
            "Allocated Zone": 120,
            "Slot ID": 150,
            "Status": 100,
            "Penalty": 80,
            "Timestamp": 150
        }
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=column_widths[col], anchor=tk.CENTER)
        
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
        
        # Add tag colors for different statuses
        self.tree.tag_configure('REQUESTED', background='#fff9e6')
        self.tree.tag_configure('ALLOCATED', background='#e8f5e9')
        self.tree.tag_configure('OCCUPIED', background='#e3f2fd')
        self.tree.tag_configure('RELEASED', background='#f3e5f5')
        self.tree.tag_configure('CANCELLED', background='#ffebee')
        
        # Context menu for actions
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Double-1>', self.show_request_details)
        
        # Load initial data
        self.refresh_status()
    
    def on_tab_selected(self):
        """Called when this tab is selected - refresh data"""
        self.refresh_status()
    
    def refresh_status(self):
        """Refresh allocation status data from parking system"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Get all requests from parking system
            requests = self.parking_system.requests.values()
            
            # Apply filter
            filter_status = self.filter_var.get()
            if filter_status != "ALL":
                requests = [r for r in requests if r.current_state.value == filter_status]
            else:
                requests = list(requests)
            
            # Update stats
            total_count = len(self.parking_system.requests)
            filtered_count = len(requests)
            self.stats_label.config(
                text=f"Showing {filtered_count} of {total_count} requests"
            )
            
            if not requests:
                # Show message if no requests
                self.tree.insert("", tk.END, values=(
                    "No requests found", "", "", "", "", "", "", ""
                ))
                return
            
            # Calculate penalty for each request
            for request in requests:
                request_id = request.request_id
                vehicle_id = request.vehicle_id
                requested_zone = request.requested_zone
                allocated_zone = request.allocated_zone if request.allocated_zone else "N/A"
                slot_id = request.allocated_slot_id if request.allocated_slot_id else "N/A"
                status = request.current_state.value
                
                # Calculate penalty
                penalty = 0
                if request.allocated_zone and request.allocated_zone != request.requested_zone:
                    # Check if adjacent or distant
                    if requested_zone in self.parking_system.zones:
                        req_zone = self.parking_system.zones[requested_zone]
                        if allocated_zone in req_zone.adjacent_zones:
                            penalty = 50  # Adjacent zone penalty
                        else:
                            penalty = 100  # Distant zone penalty
                
                # Format timestamp
                timestamp = request.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                # Insert row with color tag based on status
                self.tree.insert(
                    "", 
                    tk.END, 
                    values=(
                        request_id,
                        vehicle_id,
                        requested_zone,
                        allocated_zone,
                        slot_id,
                        status,
                        penalty,
                        timestamp
                    ),
                    tags=(status,)
                )
            
            print(f"Status screen refreshed: {filtered_count} requests displayed")
            
        except Exception as e:
            print(f"Error refreshing status: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to refresh status: {str(e)}")
    
    def sort_by_column(self, col):
        """Sort treeview by column"""
        try:
            items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
            items.sort()
            
            for index, (val, item) in enumerate(items):
                self.tree.move(item, '', index)
        except Exception as e:
            print(f"Error sorting: {e}")
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        try:
            item = self.tree.identify_row(event.y)
            if item:
                self.tree.selection_set(item)
                
                menu = tk.Menu(self, tearoff=0)
                menu.add_command(label="View Details", command=self.show_request_details)
                menu.add_separator()
                menu.add_command(label="Mark as Occupied", command=self.mark_occupied)
                menu.add_command(label="Release Parking", command=self.release_parking)
                menu.add_command(label="Cancel Request", command=self.cancel_request)
                menu.add_separator()
                menu.add_command(label="Refresh", command=self.refresh_status)
                menu.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error showing context menu: {e}")
    
    def show_request_details(self, event=None):
        """Show detailed information about selected request"""
        try:
            selection = self.tree.selection()
            if not selection:
                return
            
            item = selection[0]
            values = self.tree.item(item, 'values')
            
            if not values or values[0] == "No requests found":
                return
            
            request_id = values[0]
            request = self.parking_system.requests.get(request_id)
            
            if request:
                # Create details message
                details = f"Request Details\n"
                details += "="*40 + "\n\n"
                details += f"Request ID: {request.request_id}\n"
                details += f"Vehicle ID: {request.vehicle_id}\n"
                details += f"Requested Zone: {request.requested_zone}\n"
                details += f"Allocated Zone: {request.allocated_zone or 'N/A'}\n"
                details += f"Allocated Slot: {request.allocated_slot_id or 'N/A'}\n"
                details += f"Current Status: {request.current_state.value}\n"
                details += f"Penalty: {values[6]}\n"
                details += f"Request Time: {request.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                if request.allocation_timestamp:
                    details += f"Allocation Time: {request.allocation_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                if request.release_timestamp:
                    details += f"Release Time: {request.release_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    duration = request.get_parking_duration()
                    if duration:
                        hours = duration // 3600
                        minutes = (duration % 3600) // 60
                        seconds = duration % 60
                        details += f"Parking Duration: {hours}h {minutes}m {seconds}s\n"
                
                messagebox.showinfo("Request Details", details)
        except Exception as e:
            print(f"Error showing details: {e}")
            messagebox.showerror("Error", "Failed to show request details")
    
    # ========== PARKING OPERATIONS ==========
    
    def get_selected_request_id(self):
        """Get the request ID of the selected item"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a request first")
            return None
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        
        if not values or values[0] == "No requests found":
            return None
        
        return values[0]
    
    def mark_occupied(self):
        """Mark an allocated parking slot as occupied"""
        request_id = self.get_selected_request_id()
        if not request_id:
            return
        
        try:
            request = self.parking_system.requests.get(request_id)
            
            if not request:
                messagebox.showerror("Error", f"Request {request_id} not found")
                return
            
            # Check current state
            if request.current_state != RequestState.ALLOCATED:
                messagebox.showerror(
                    "Invalid Operation",
                    f"Cannot mark as occupied. Current state: {request.current_state.value}\n"
                    "Only ALLOCATED requests can be marked as occupied."
                )
                return
            
            # Confirm action
            confirm = messagebox.askyesno(
                "Confirm Action",
                f"Mark request {request_id} as OCCUPIED?\n\n"
                f"Vehicle: {request.vehicle_id}\n"
                f"Slot: {request.allocated_slot_id}"
            )
            
            if not confirm:
                return
            
            # Call parking system method
            result = self.parking_system.mark_parking_occupied(request_id)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                self.refresh_status()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
                
        except Exception as e:
            print(f"Error marking as occupied: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to mark as occupied: {str(e)}")
    
    def release_parking(self):
        """Release an occupied parking slot"""
        request_id = self.get_selected_request_id()
        if not request_id:
            return
        
        try:
            request = self.parking_system.requests.get(request_id)
            
            if not request:
                messagebox.showerror("Error", f"Request {request_id} not found")
                return
            
            # Check current state
            if request.current_state != RequestState.OCCUPIED:
                messagebox.showerror(
                    "Invalid Operation",
                    f"Cannot release parking. Current state: {request.current_state.value}\n"
                    "Only OCCUPIED requests can be released."
                )
                return
            
            # Confirm action
            confirm = messagebox.askyesno(
                "Confirm Action",
                f"Release parking for request {request_id}?\n\n"
                f"Vehicle: {request.vehicle_id}\n"
                f"Slot: {request.allocated_slot_id}"
            )
            
            if not confirm:
                return
            
            # Call parking system method
            result = self.parking_system.release_parking(request_id)
            
            if result['success']:
                # Show duration if available
                message = result['message']
                if 'duration_seconds' in result:
                    duration = result['duration_seconds']
                    hours = duration // 3600
                    minutes = (duration % 3600) // 60
                    seconds = duration % 60
                    message += f"\n\nParking Duration: {hours}h {minutes}m {seconds}s"
                
                messagebox.showinfo("Success", message)
                self.refresh_status()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
                
        except Exception as e:
            print(f"Error releasing parking: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to release parking: {str(e)}")
    
    def cancel_request(self):
        """Cancel a parking request"""
        request_id = self.get_selected_request_id()
        if not request_id:
            return
        
        try:
            request = self.parking_system.requests.get(request_id)
            
            if not request:
                messagebox.showerror("Error", f"Request {request_id} not found")
                return
            
            # Check current state
            if request.current_state in [RequestState.RELEASED, RequestState.CANCELLED]:
                messagebox.showerror(
                    "Invalid Operation",
                    f"Cannot cancel. Current state: {request.current_state.value}\n"
                    "Request is already completed or cancelled."
                )
                return
            
            if request.current_state == RequestState.OCCUPIED:
                messagebox.showerror(
                    "Invalid Operation",
                    "Cannot cancel an OCCUPIED request.\n"
                    "Please release the parking first."
                )
                return
            
            # Confirm action
            confirm = messagebox.askyesno(
                "Confirm Action",
                f"Cancel request {request_id}?\n\n"
                f"Vehicle: {request.vehicle_id}\n"
                f"Status: {request.current_state.value}\n"
                f"Slot: {request.allocated_slot_id or 'Not allocated'}\n\n"
                "This action will be recorded in rollback history."
            )
            
            if not confirm:
                return
            
            # Call parking system method
            result = self.parking_system.cancel_parking_request(request_id)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                self.refresh_status()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
                
        except Exception as e:
            print(f"Error cancelling request: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to cancel request: {str(e)}")
    
    def refresh_dashboard(self):
        """Refresh the dashboard in the parent window if it exists"""
        try:
            parent = self.master
            while parent:
                if hasattr(parent, 'dashboard'):
                    parent.dashboard.refresh_stats()
                    break
                parent = parent.master if hasattr(parent, 'master') else None
        except Exception as e:
            print(f"Could not refresh dashboard: {e}")
