"""
Main Application Window for SmartPark
Manages navigation between different screens
"""
import tkinter as tk
from tkinter import ttk
from ui.dashboard_screen import DashboardScreen
from ui.request_screen import RequestScreen
from ui.setup_screen import SetupScreen
from ui.status_screen import StatusScreen
from ui.rollback_screen import RollbackScreen
from ui.analytics_screen import AnalyticsScreen


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
        self.root.geometry("1200x750")
        
        # Modern color scheme
        self.colors = {
            'primary': '#2563eb',      # Blue
            'secondary': '#10b981',    # Green
            'danger': '#ef4444',       # Red
            'warning': '#f59e0b',      # Orange
            'info': '#3b82f6',         # Light Blue
            'success': '#22c55e',      # Light Green
            'dark': '#1e293b',         # Dark Blue Gray
            'light': '#f8fafc',        # Light Gray
            'gray': '#64748b',         # Medium Gray
            'card_bg': '#ffffff'       # White
        }
        
        # Set minimum window size
        self.root.minsize(1000, 650)
        
        # Set background color
        self.root.configure(bg=self.colors['light'])
        
        # Create main container
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the main UI components"""
        # Header with modern styling
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=100)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)  # Maintain height
        
        # Title with icon
        title_label = tk.Label(
            header_frame,
            text="🅿️ SmartPark Management System",
            font=("Segoe UI", 26, "bold"),
            bg=self.colors['dark'],
            fg="white"
        )
        title_label.pack(pady=25)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Intelligent Parking Allocation with DSA",
            font=("Segoe UI", 10),
            bg=self.colors['dark'],
            fg=self.colors['gray']
        )
        subtitle_label.pack()
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['light'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10], 
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['card_bg'],
                       foreground=self.colors['dark'])
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')],
                 padding=[('selected', [25, 12])],  # Larger padding for selected tab
                 expand=[('selected', [1, 1, 1, 0])])
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
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
        
        # Allocation Status Tab - Fully integrated
        status_frame = StatusScreen(self.notebook, self.parking_system)
        self.notebook.add(status_frame, text="📍 Allocation Status")
        
        # Store reference
        self.status_screen = status_frame
        
        # Rollback Tab - Fully integrated
        rollback_frame = RollbackScreen(self.notebook, self.parking_system)
        self.notebook.add(rollback_frame, text="↩️ Rollback")
        
        # Store reference
        self.rollback_screen = rollback_frame
        
        # Analytics Tab - Fully integrated
        analytics_frame = AnalyticsScreen(self.notebook, self.parking_system)
        self.notebook.add(analytics_frame, text="📈 Analytics")
        
        # Store reference
        self.analytics_screen = analytics_frame
    
    def on_tab_changed(self, event):
        """Handle tab change events to refresh screen data"""
        try:
            # Get the currently selected tab index
            selected_tab = self.notebook.select()
            tab_index = self.notebook.index(selected_tab)
            
            # Refresh appropriate screen based on tab index
            # Tab 0: Setup, Tab 1: Dashboard, Tab 2: Request, Tab 3: Status, Tab 4: Rollback, Tab 5: Analytics
            if tab_index == 1 and hasattr(self, 'dashboard'):
                # Refresh dashboard
                self.dashboard.refresh_stats()
            elif tab_index == 2 and hasattr(self, 'request_screen'):
                # Refresh request screen zone list
                self.request_screen.on_tab_selected()
            elif tab_index == 3 and hasattr(self, 'status_screen'):
                # Refresh status screen
                self.status_screen.on_tab_selected()
            elif tab_index == 4 and hasattr(self, 'rollback_screen'):
                # Refresh rollback screen
                self.rollback_screen.on_tab_selected()
            elif tab_index == 5 and hasattr(self, 'analytics_screen'):
                # Refresh analytics screen
                self.analytics_screen.on_tab_selected()
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
