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
        """Load available zones into combobox"""
        # TODO: Get zones from parking_system
        # For now, placeholder
        self.zone_combobox['values'] = ['ZONE-A', 'ZONE-B', 'ZONE-C']
        if self.zone_combobox['values']:
            self.zone_combobox.current(0)
    
    def on_request_parking(self):
        """Handle parking request submission"""
        vehicle_id = self.vehicle_id_entry.get().strip()
        zone_id = self.zone_combobox.get()
        
        if not vehicle_id:
            messagebox.showerror("Error", "Please enter a Vehicle ID")
            return
        
        if not zone_id:
            messagebox.showerror("Error", "Please select a zone")
            return
        
        # TODO: Call parking_system.create_request(vehicle_id, zone_id)
        messagebox.showinfo(
            "Success",
            f"Parking request created for {vehicle_id} in {zone_id}"
        )
        
        # Clear form
        self.vehicle_id_entry.delete(0, tk.END)
