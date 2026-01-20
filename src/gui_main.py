"""
GUI Entry Point for SmartPark
Launches the Tkinter application
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parking_system import ParkingSystem
from ui.main_window import MainWindow


def main():
    """Main entry point for GUI application"""
    print("="*60)
    print("SmartPark - Parking Management System")
    print("="*60)
    print("\nStarting GUI...")
    print("Use the Setup tab to configure zones, areas, and vehicles")
    print("="*60)
    
    # Initialize parking system
    parking_system = ParkingSystem()
    
    # Create and run GUI
    app = MainWindow(parking_system)
    app.run()


if __name__ == "__main__":
    main()
