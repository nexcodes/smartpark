"""
Parking Request Screen
Allows users to create new parking requests
"""
import tkinter as tk
from tkinter import ttk, messagebox


class RequestScreen(tk.Frame):
    """Screen for creating new parking requests"""
    
    def __init__(self, parent, parking_system):
        """
        Initialize request screen
        
        Args:
            parent: Parent widget
            parking_system: ParkingSystem instance
        """
        super().__init__(parent)
        self.parking_system = parking_system
        self.setup_ui()
    
    def setup_ui(self):
        """Set up request screen UI components"""
        # Background
        self.configure(bg='#f8fafc')
        
        # Title section
        title_frame = tk.Frame(self, bg='#f8fafc')
        title_frame.pack(pady=25, padx=30, fill=tk.X)
        
        title = tk.Label(
            title_frame,
            text="🚗 Create Parking Request",
            font=("Segoe UI", 24, "bold"),
            fg="#1e293b",
            bg='#f8fafc'
        )
        title.pack(anchor='w')
        
        subtitle = tk.Label(
            title_frame,
            text="Request a parking slot for your vehicle",
            font=("Segoe UI", 10),
            fg="#64748b",
            bg='#f8fafc'
        )
        subtitle.pack(anchor='w', pady=(5, 0))
        
        # Form card with modern design
        card_frame = tk.Frame(self, bg='white', highlightbackground="#e2e8f0", highlightthickness=1)
        card_frame.pack(pady=20, padx=100, fill=tk.BOTH, expand=True)
        
        # Form content
        form_frame = tk.Frame(card_frame, bg='white')
        form_frame.pack(pady=40, padx=50, fill=tk.BOTH, expand=True)
        
        # Vehicle ID
        tk.Label(form_frame, text="Vehicle ID", font=("Segoe UI", 12, "bold"), 
                bg='white', fg='#1e293b').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5), padx=10
        )
        
        # Style for combobox
        style = ttk.Style()
        style.configure('Modern.TCombobox', padding=5)
        
        self.vehicle_id_combobox = ttk.Combobox(
            form_frame,
            font=("Segoe UI", 11),
            width=35,
            state="readonly",
            style='Modern.TCombobox'
        )
        self.vehicle_id_combobox.grid(row=1, column=0, pady=(0, 20), padx=10, sticky='ew')
        
        # Zone selection
        tk.Label(form_frame, text="Preferred Zone", font=("Segoe UI", 12, "bold"),
                bg='white', fg='#1e293b').grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5), padx=10
        )
        self.zone_combobox = ttk.Combobox(
            form_frame,
            font=("Segoe UI", 11),
            width=35,
            state="readonly",
            style='Modern.TCombobox'
        )
        self.zone_combobox.grid(row=3, column=0, pady=(0, 30), padx=10, sticky='ew')
        
        # Configure grid column
        form_frame.grid_columnconfigure(0, weight=1)
        
        # Submit button with modern design
        submit_btn = tk.Button(
            form_frame,
            text="🅿️ Request Parking Slot",
            font=("Segoe UI", 13, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.on_request_parking
        )
        submit_btn.grid(row=4, column=0, pady=20, padx=10)
        
        # Load available zones and vehicles
        self.load_zones()
        self.load_vehicles()
    
    def on_tab_selected(self):
        """Called when this tab is selected - refresh data"""
        self.load_zones()
        self.load_vehicles()
    
    def load_vehicles(self):
        """Load registered vehicles from parking system"""
        try:
            # Get vehicles from parking system
            vehicle_ids = list(self.parking_system.vehicles.keys())
            
            if vehicle_ids:
                # Store current selection if any
                current = self.vehicle_id_combobox.get()
                self.vehicle_id_combobox['values'] = vehicle_ids
                
                # Restore previous selection if still valid, otherwise select first
                if current in vehicle_ids:
                    self.vehicle_id_combobox.set(current)
                else:
                    self.vehicle_id_combobox.current(0)
            else:
                self.vehicle_id_combobox['values'] = []
                self.vehicle_id_combobox.set('')
        except Exception as e:
            print(f"Error loading vehicles: {e}")
    
    def load_zones(self):
        """Load available zones from parking system"""
        try:
            # Get zones from parking system
            zone_ids = list(self.parking_system.zones.keys())
            
            if zone_ids:
                # Store current selection if any
                current = self.zone_combobox.get()
                self.zone_combobox['values'] = zone_ids
                
                # Restore previous selection if still valid, otherwise select first
                if current in zone_ids:
                    self.zone_combobox.set(current)
                else:
                    self.zone_combobox.current(0)
            else:
                self.zone_combobox['values'] = []
                self.zone_combobox.set('')
        except Exception as e:
            print(f"Error loading zones: {e}")
    
    def on_request_parking(self):
        """Handle parking request submission"""
        vehicle_id = self.vehicle_id_combobox.get().strip()
        zone_id = self.zone_combobox.get()
        
        # Validation
        if not vehicle_id:
            messagebox.showerror("Error", "Please select a Vehicle ID")
            return
        
        if not zone_id:
            messagebox.showerror("Error", "Please select a zone")
            return
        
        try:
            # Vehicle should already be registered (selected from dropdown)
            if vehicle_id not in self.parking_system.vehicles:
                messagebox.showerror(
                    "Error",
                    f"Vehicle {vehicle_id} not found. Please register it in Setup tab first."
                )
                return
            
            # Create parking request
            request_result = self.parking_system.create_parking_request(vehicle_id, zone_id)
            
            if request_result['success']:
                request_id = request_result['request_id']
                
                # Automatically try to allocate parking
                allocation_result = self.parking_system.allocate_parking(request_id)
                
                if allocation_result['success']:
                    slot_id = allocation_result['slot_id']
                    penalty = allocation_result.get('penalty', 0)
                    
                    message = f"✓ Parking Allocated!\n\n"
                    message += f"Request ID: {request_id}\n"
                    message += f"Vehicle: {vehicle_id}\n"
                    message += f"Slot: {slot_id}\n"
                    message += f"Zone: {zone_id}\n"
                    
                    if penalty > 0:
                        message += f"\nCross-zone penalty: {penalty}"
                    
                    messagebox.showinfo("Allocation Successful", message)
                else:
                    # Request created but allocation failed
                    message = f"Request created but allocation failed:\n\n"
                    message += f"Request ID: {request_id}\n"
                    message += f"Reason: {allocation_result['message']}"
                    messagebox.showwarning("Allocation Failed", message)
                
                # Clear form (reset to first vehicle)
                if self.vehicle_id_combobox['values']:
                    self.vehicle_id_combobox.current(0)
                
                # Refresh dashboard if it exists
                self.refresh_parent_dashboard()
            else:
                messagebox.showerror("Error", request_result['message'])
                
        except Exception as e:
            print(f"Error creating parking request: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to create parking request: {str(e)}")
    
    def refresh_parent_dashboard(self):
        """Refresh the dashboard in the parent window if it exists"""
        try:
            # Navigate up to find the main window
            parent = self.master
            while parent:
                if hasattr(parent, 'dashboard'):
                    parent.dashboard.refresh_stats()
                    break
                parent = parent.master if hasattr(parent, 'master') else None
        except Exception as e:
            print(f"Could not refresh dashboard: {e}")
