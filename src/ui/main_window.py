"""
Main Application Window for SmartPark
Manages navigation between different screens
"""
import tkinter as tk
from tkinter import ttk
from ui.dashboard_screen import DashboardScreen
from ui.request_screen import RequestScreen
from ui.setup_screen import SetupScreen


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
        
        # Bind tab change event to refresh screens
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Placeholder tabs - will be replaced with actual screens
        self.setup_tabs()
    
    def setup_tabs(self):
        """Create all tabs for different screens"""
        # Setup Tab - System Configuration (First tab)
        setup_frame = SetupScreen(self.notebook, self.parking_system)
        self.notebook.add(setup_frame, text="⚙️ Setup")
        
        # Store reference
        self.setup_screen = setup_frame
        
        # Dashboard Tab - Fully integrated
        dashboard_frame = DashboardScreen(self.notebook, self.parking_system)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Store reference for refreshing
        self.dashboard = dashboard_frame
        
        # Parking Request Tab - Fully integrated
        request_frame = RequestScreen(self.notebook, self.parking_system)
        self.notebook.add(request_frame, text="🚗 New Request")
        
        # Store reference
        self.request_screen = request_frame
        
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
    
    def on_tab_changed(self, event):
        """Handle tab change events to refresh screen data"""
        try:
            # Get the currently selected tab index
            selected_tab = self.notebook.select()
            tab_index = self.notebook.index(selected_tab)
            
            # Refresh appropriate screen based on tab index
            # Tab 0: Setup, Tab 1: Dashboard, Tab 2: Request, etc.
            if tab_index == 1 and hasattr(self, 'dashboard'):
                # Refresh dashboard
                self.dashboard.refresh_stats()
            elif tab_index == 2 and hasattr(self, 'request_screen'):
                # Refresh request screen zone list
                self.request_screen.on_tab_selected()
        except Exception as e:
            print(f"Error in tab change: {e}")
    
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
