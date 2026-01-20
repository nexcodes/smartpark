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
        # Title
        title = tk.Label(
            self,
            text="Create Parking Request",
            font=("Arial", 20, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self)
        form_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # Vehicle ID
        tk.Label(form_frame, text="Vehicle ID:", font=("Arial", 12)).grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=10
        )
        self.vehicle_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.vehicle_id_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Zone selection
        tk.Label(form_frame, text="Preferred Zone:", font=("Arial", 12)).grid(
            row=1, column=0, sticky=tk.W, pady=10, padx=10
        )
        self.zone_combobox = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=28,
            state="readonly"
        )
        self.zone_combobox.grid(row=1, column=1, pady=10, padx=10)
        
        # Submit button
        submit_btn = tk.Button(
            form_frame,
            text="Request Parking",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            width=20,
            command=self.on_request_parking
        )
        submit_btn.grid(row=2, column=0, columnspan=2, pady=30)
        
        # Load available zones
        self.load_zones()
    
    def load_zones(self):
        """Load available zones from parking system"""
        try:
            # Get zones from parking system
            zone_ids = list(self.parking_system.zones.keys())
            
            if zone_ids:
                self.zone_combobox['values'] = zone_ids
                self.zone_combobox.current(0)
            else:
                self.zone_combobox['values'] = []
                messagebox.showwarning(
                    "No Zones",
                    "No parking zones available. Please set up zones first."
                )
        except Exception as e:
            print(f"Error loading zones: {e}")
            messagebox.showerror("Error", "Failed to load parking zones")
    
    def on_request_parking(self):
        """Handle parking request submission"""
        vehicle_id = self.vehicle_id_entry.get().strip().upper()
        zone_id = self.zone_combobox.get()
        
        # Validation
        if not vehicle_id:
            messagebox.showerror("Error", "Please enter a Vehicle ID")
            return
        
        if not zone_id:
            messagebox.showerror("Error", "Please select a zone")
            return
        
        try:
            # Register vehicle if not already registered
            if vehicle_id not in self.parking_system.vehicles:
                vehicle_result = self.parking_system.register_vehicle(vehicle_id, zone_id)
                if not vehicle_result['success']:
                    messagebox.showerror("Error", vehicle_result['message'])
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
                
                # Clear form
                self.vehicle_id_entry.delete(0, tk.END)
                
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
