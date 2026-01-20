"""
Main Application Window for SmartPark
Manages navigation between different screens
"""
import tkinter as tk
from tkinter import ttk


class MainWindow:
    """Main application window with tabbed navigation"""
    
    def __init__(self, parking_system):
        """
        Initialize main window
        
        Args:
            parking_system: ParkingSystem instance (backend logic)
        """
        self.parking_system = parking_system
        self.root = tk.Tk()
        self.root.title("SmartPark - Parking Management System")
        self.root.geometry("1000x700")
        
        # Create main container
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the main UI components"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        title_label = tk.Label(
            header_frame,
            text="SmartPark Management System",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Placeholder tabs - will be replaced with actual screens
        self.setup_tabs()
    
    def setup_tabs(self):
        """Create all tabs for different screens"""
        # Dashboard Tab
        dashboard_frame = tk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        self.create_placeholder(dashboard_frame, "Main Dashboard")
        
        # Parking Request Tab
        request_frame = tk.Frame(self.notebook)
        self.notebook.add(request_frame, text="🚗 New Request")
        self.create_placeholder(request_frame, "Parking Request Screen")
        
        # Allocation Status Tab
        status_frame = tk.Frame(self.notebook)
        self.notebook.add(status_frame, text="📍 Allocation Status")
        self.create_placeholder(status_frame, "Allocation Status Screen")
        
        # Rollback Tab
        rollback_frame = tk.Frame(self.notebook)
        self.notebook.add(rollback_frame, text="↩️ Rollback")
        self.create_placeholder(rollback_frame, "Cancellation & Rollback Screen")
        
        # Analytics Tab
        analytics_frame = tk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="📈 Analytics")
        self.create_placeholder(analytics_frame, "Analytics Screen")
    
    def create_placeholder(self, parent, text):
        """Create placeholder content for tabs"""
        label = tk.Label(
            parent,
            text=f"{text}\n(Under Construction)",
            font=("Arial", 18),
            fg="#7f8c8d"
        )
        label.pack(expand=True)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
