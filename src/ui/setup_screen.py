"""
Setup/Configuration Screen
Handles system setup operations: zones, areas, adjacency, and vehicle registration
"""
import tkinter as tk
from tkinter import ttk, messagebox


class SetupScreen(tk.Frame):
    """Screen for system configuration and setup"""
    
    def __init__(self, parent, parking_system):
        """
        Initialize setup screen
        
        Args:
            parent: Parent widget
            parking_system: ParkingSystem instance
        """
        super().__init__(parent)
        self.parking_system = parking_system
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the configuration UI components"""
        # Title
        title = tk.Label(
            self,
            text="System Setup & Configuration",
            font=("Arial", 20, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Create notebook for different setup sections
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Zone Management Tab
        zone_frame = tk.Frame(notebook)
        notebook.add(zone_frame, text="Zones")
        self.setup_zone_tab(zone_frame)
        
        # Parking Area Tab
        area_frame = tk.Frame(notebook)
        notebook.add(area_frame, text="Parking Areas")
        self.setup_area_tab(area_frame)
        
        # Zone Adjacency Tab
        adjacency_frame = tk.Frame(notebook)
        notebook.add(adjacency_frame, text="Zone Adjacency")
        self.setup_adjacency_tab(adjacency_frame)
        
        # Vehicle Registration Tab
        vehicle_frame = tk.Frame(notebook)
        notebook.add(vehicle_frame, text="Vehicles")
        self.setup_vehicle_tab(vehicle_frame)
    
    def setup_zone_tab(self, parent):
        """Set up zone management tab"""
        # Instructions
        instruction = tk.Label(
            parent,
            text="Create new parking zones in the system",
            font=("Arial", 11),
            fg="#7f8c8d"
        )
        instruction.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(parent)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Zone ID:", font=("Arial", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.E
        )
        
        self.zone_id_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.zone_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Example text
        example = tk.Label(
            input_frame,
            text="e.g., ZONE-A, ZONE-B, ZONE-C",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        example.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="Add Zone",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=15,
            command=self.add_zone
        )
        add_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Existing zones list
        list_frame = tk.LabelFrame(
            parent,
            text="Existing Zones",
            font=("Arial", 11, "bold")
        )
        list_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        self.zone_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 11),
            height=8
        )
        self.zone_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            list_frame,
            text="Refresh List",
            font=("Arial", 10),
            command=self.refresh_zone_list
        )
        refresh_btn.pack(pady=5)
        
        # Initial load
        self.refresh_zone_list()
    
    def setup_area_tab(self, parent):
        """Set up parking area management tab"""
        # Instructions
        instruction = tk.Label(
            parent,
            text="Add parking areas with slots to existing zones",
            font=("Arial", 11),
            fg="#7f8c8d"
        )
        instruction.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(parent)
        input_frame.pack(pady=20)
        
        # Zone selection
        tk.Label(input_frame, text="Zone:", font=("Arial", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.E
        )
        
        self.area_zone_combobox = ttk.Combobox(
            input_frame,
            font=("Arial", 12),
            width=23,
            state="readonly"
        )
        self.area_zone_combobox.grid(row=0, column=1, padx=10, pady=10)
        
        # Area ID
        tk.Label(input_frame, text="Area ID:", font=("Arial", 12, "bold")).grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.E
        )
        
        self.area_id_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.area_id_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Capacity
        tk.Label(input_frame, text="Capacity:", font=("Arial", 12, "bold")).grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.E
        )
        
        self.capacity_spinbox = tk.Spinbox(
            input_frame,
            from_=1,
            to=100,
            font=("Arial", 12),
            width=23
        )
        self.capacity_spinbox.grid(row=2, column=1, padx=10, pady=10)
        
        # Example text
        example = tk.Label(
            input_frame,
            text="e.g., Area ID: A1, Capacity: 10",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        example.grid(row=3, column=1, sticky=tk.W, padx=10)
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="Add Parking Area",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=20,
            command=self.add_parking_area
        )
        add_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Load zones
        self.refresh_area_zone_list()
    
    def setup_adjacency_tab(self, parent):
        """Set up zone adjacency tab"""
        # Instructions
        instruction = tk.Label(
            parent,
            text="Link two zones as adjacent (bidirectional)",
            font=("Arial", 11),
            fg="#7f8c8d"
        )
        instruction.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(parent)
        input_frame.pack(pady=20)
        
        # Zone 1
        tk.Label(input_frame, text="Zone 1:", font=("Arial", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.E
        )
        
        self.zone1_combobox = ttk.Combobox(
            input_frame,
            font=("Arial", 12),
            width=23,
            state="readonly"
        )
        self.zone1_combobox.grid(row=0, column=1, padx=10, pady=10)
        
        # Zone 2
        tk.Label(input_frame, text="Zone 2:", font=("Arial", 12, "bold")).grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.E
        )
        
        self.zone2_combobox = ttk.Combobox(
            input_frame,
            font=("Arial", 12),
            width=23,
            state="readonly"
        )
        self.zone2_combobox.grid(row=1, column=1, padx=10, pady=10)
        
        # Link button
        link_btn = tk.Button(
            input_frame,
            text="Link Zones",
            font=("Arial", 12, "bold"),
            bg="#e67e22",
            fg="white",
            width=20,
            command=self.link_zones
        )
        link_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Adjacency display
        display_frame = tk.LabelFrame(
            parent,
            text="Current Adjacency Links",
            font=("Arial", 11, "bold")
        )
        display_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        self.adjacency_text = tk.Text(
            display_frame,
            height=10,
            font=("Courier", 10),
            state=tk.DISABLED
        )
        self.adjacency_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            display_frame,
            text="Refresh Adjacency",
            font=("Arial", 10),
            command=self.refresh_adjacency_display
        )
        refresh_btn.pack(pady=5)
        
        # Load zones
        self.refresh_adjacency_zone_lists()
    
    def setup_vehicle_tab(self, parent):
        """Set up vehicle registration tab"""
        # Instructions
        instruction = tk.Label(
            parent,
            text="Register vehicles in the system",
            font=("Arial", 11),
            fg="#7f8c8d"
        )
        instruction.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(parent)
        input_frame.pack(pady=20)
        
        # Vehicle ID
        tk.Label(input_frame, text="Vehicle ID:", font=("Arial", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.E
        )
        
        self.vehicle_id_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.vehicle_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Preferred Zone
        tk.Label(input_frame, text="Preferred Zone:", font=("Arial", 12, "bold")).grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.E
        )
        
        self.vehicle_zone_combobox = ttk.Combobox(
            input_frame,
            font=("Arial", 12),
            width=23,
            state="readonly"
        )
        self.vehicle_zone_combobox.grid(row=1, column=1, padx=10, pady=10)
        
        # Example text
        example = tk.Label(
            input_frame,
            text="e.g., CAR-001, BIKE-123, TRUCK-456",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        example.grid(row=2, column=1, sticky=tk.W, padx=10)
        
        # Register button
        register_btn = tk.Button(
            input_frame,
            text="Register Vehicle",
            font=("Arial", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            width=20,
            command=self.register_vehicle
        )
        register_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Registered vehicles list
        list_frame = tk.LabelFrame(
            parent,
            text="Registered Vehicles",
            font=("Arial", 11, "bold")
        )
        list_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        self.vehicle_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 11),
            height=8
        )
        self.vehicle_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            list_frame,
            text="Refresh List",
            font=("Arial", 10),
            command=self.refresh_vehicle_list
        )
        refresh_btn.pack(pady=5)
        
        # Load zones and vehicles
        self.refresh_vehicle_zone_list()
        self.refresh_vehicle_list()
    
    # ========== ZONE OPERATIONS ==========
    
    def add_zone(self):
        """Add a new zone"""
        zone_id = self.zone_id_entry.get().strip().upper()
        
        if not zone_id:
            messagebox.showerror("Error", "Please enter a Zone ID")
            return
        
        try:
            result = self.parking_system.add_zone(zone_id)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                self.zone_id_entry.delete(0, tk.END)
                self.refresh_zone_list()
                self.refresh_all_zone_lists()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add zone: {str(e)}")
    
    def refresh_zone_list(self):
        """Refresh the zone listbox"""
        self.zone_listbox.delete(0, tk.END)
        
        zones = list(self.parking_system.zones.keys())
        if zones:
            for zone_id in zones:
                zone_status = self.parking_system.get_zone_status(zone_id)
                if zone_status:
                    capacity = zone_status['total_capacity']
                    available = zone_status['available']
                    self.zone_listbox.insert(
                        tk.END,
                        f"{zone_id}: {capacity} slots ({available} available)"
                    )
        else:
            self.zone_listbox.insert(tk.END, "No zones created yet")
    
    # ========== PARKING AREA OPERATIONS ==========
    
    def add_parking_area(self):
        """Add a parking area to a zone"""
        zone_id = self.area_zone_combobox.get()
        area_id = self.area_id_entry.get().strip().upper()
        
        if not zone_id:
            messagebox.showerror("Error", "Please select a zone")
            return
        
        if not area_id:
            messagebox.showerror("Error", "Please enter an Area ID")
            return
        
        try:
            capacity = int(self.capacity_spinbox.get())
            if capacity < 1:
                raise ValueError("Capacity must be at least 1")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid capacity (1-100)")
            return
        
        try:
            result = self.parking_system.add_parking_area_to_zone(zone_id, area_id, capacity)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                self.area_id_entry.delete(0, tk.END)
                self.capacity_spinbox.delete(0, tk.END)
                self.capacity_spinbox.insert(0, "10")
                self.refresh_zone_list()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add parking area: {str(e)}")
    
    def refresh_area_zone_list(self):
        """Refresh zone combobox for parking areas"""
        zones = list(self.parking_system.zones.keys())
        self.area_zone_combobox['values'] = zones
        if zones:
            self.area_zone_combobox.current(0)
    
    # ========== ADJACENCY OPERATIONS ==========
    
    def link_zones(self):
        """Link two zones as adjacent"""
        zone1_id = self.zone1_combobox.get()
        zone2_id = self.zone2_combobox.get()
        
        if not zone1_id or not zone2_id:
            messagebox.showerror("Error", "Please select both zones")
            return
        
        if zone1_id == zone2_id:
            messagebox.showerror("Error", "Cannot link a zone to itself")
            return
        
        try:
            result = self.parking_system.link_adjacent_zones(zone1_id, zone2_id)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                self.refresh_adjacency_display()
            else:
                messagebox.showerror("Error", result['message'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to link zones: {str(e)}")
    
    def refresh_adjacency_zone_lists(self):
        """Refresh zone comboboxes for adjacency"""
        zones = list(self.parking_system.zones.keys())
        self.zone1_combobox['values'] = zones
        self.zone2_combobox['values'] = zones
        if zones:
            self.zone1_combobox.current(0)
            if len(zones) > 1:
                self.zone2_combobox.current(1)
            else:
                self.zone2_combobox.current(0)
        self.refresh_adjacency_display()
    
    def refresh_adjacency_display(self):
        """Refresh adjacency display"""
        self.adjacency_text.config(state=tk.NORMAL)
        self.adjacency_text.delete(1.0, tk.END)
        
        zones = self.parking_system.zones
        if not zones:
            self.adjacency_text.insert(tk.END, "No zones available")
        else:
            for zone_id, zone in zones.items():
                adjacent = zone.adjacent_zones
                if adjacent:
                    self.adjacency_text.insert(
                        tk.END,
                        f"{zone_id} ↔ {', '.join(adjacent)}\n"
                    )
                else:
                    self.adjacency_text.insert(
                        tk.END,
                        f"{zone_id} (no adjacent zones)\n"
                    )
        
        self.adjacency_text.config(state=tk.DISABLED)
    
    # ========== VEHICLE OPERATIONS ==========
    
    def register_vehicle(self):
        """Register a vehicle"""
        vehicle_id = self.vehicle_id_entry.get().strip().upper()
        preferred_zone = self.vehicle_zone_combobox.get()
        
        if not vehicle_id:
            messagebox.showerror("Error", "Please enter a Vehicle ID")
            return
        
        try:
            result = self.parking_system.register_vehicle(vehicle_id, preferred_zone)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                self.vehicle_id_entry.delete(0, tk.END)
                self.refresh_vehicle_list()
            else:
                messagebox.showerror("Error", result['message'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register vehicle: {str(e)}")
    
    def refresh_vehicle_zone_list(self):
        """Refresh zone combobox for vehicles"""
        zones = list(self.parking_system.zones.keys())
        self.vehicle_zone_combobox['values'] = [''] + zones  # Allow no preferred zone
        if zones:
            self.vehicle_zone_combobox.current(0)
    
    def refresh_vehicle_list(self):
        """Refresh the vehicle listbox"""
        self.vehicle_listbox.delete(0, tk.END)
        
        vehicles = self.parking_system.vehicles
        if vehicles:
            for vehicle_id, vehicle in vehicles.items():
                pref_zone = vehicle.preferred_zone if vehicle.preferred_zone else "None"
                self.vehicle_listbox.insert(
                    tk.END,
                    f"{vehicle_id}: Preferred Zone = {pref_zone}"
                )
        else:
            self.vehicle_listbox.insert(tk.END, "No vehicles registered yet")
    
    # ========== HELPER METHODS ==========
    
    def refresh_all_zone_lists(self):
        """Refresh all zone-related dropdowns"""
        self.refresh_area_zone_list()
        self.refresh_adjacency_zone_lists()
        self.refresh_vehicle_zone_list()
    
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
