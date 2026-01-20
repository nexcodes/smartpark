"""
Rollback Screen
Handles cancellation and rollback operations
"""
import tkinter as tk
from tkinter import ttk, messagebox


class RollbackScreen(tk.Frame):
    """Screen for cancellation and rollback operations"""
    
    def __init__(self, parent, parking_system):
        """
        Initialize rollback screen
        
        Args:
            parent: Parent widget
            parking_system: ParkingSystem instance
        """
        super().__init__(parent)
        self.parking_system = parking_system
        self.setup_ui()
    
    def setup_ui(self):
        """Set up rollback screen UI components"""
        # Title
        title = tk.Label(
            self,
            text="Cancellation & Rollback",
            font=("Arial", 20, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Cancel Request Section
        cancel_frame = tk.LabelFrame(
            self,
            text="Cancel Request",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=20
        )
        cancel_frame.pack(pady=20, padx=50, fill=tk.X)
        
        tk.Label(cancel_frame, text="Request ID:", font=("Arial", 12)).grid(
            row=0, column=0, sticky=tk.W, pady=10
        )
        self.request_id_entry = tk.Entry(cancel_frame, font=("Arial", 12), width=20)
        self.request_id_entry.grid(row=0, column=1, pady=10, padx=10)
        
        cancel_btn = tk.Button(
            cancel_frame,
            text="Cancel Request",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            command=self.on_cancel_request
        )
        cancel_btn.grid(row=0, column=2, pady=10, padx=10)
        
        # Rollback Section
        rollback_frame = tk.LabelFrame(
            self,
            text="Rollback Operations",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=20
        )
        rollback_frame.pack(pady=20, padx=50, fill=tk.X)
        
        tk.Label(rollback_frame, text="Number of Operations:", font=("Arial", 12)).grid(
            row=0, column=0, sticky=tk.W, pady=10
        )
        self.rollback_count_spinbox = tk.Spinbox(
            rollback_frame,
            from_=1,
            to=100,
            font=("Arial", 12),
            width=18
        )
        self.rollback_count_spinbox.grid(row=0, column=1, pady=10, padx=10)
        
        rollback_btn = tk.Button(
            rollback_frame,
            text="Rollback",
            font=("Arial", 12),
            bg="#f39c12",
            fg="white",
            command=self.on_rollback
        )
        rollback_btn.grid(row=0, column=2, pady=10, padx=10)
        
        # Operation History
        history_frame = tk.LabelFrame(
            self,
            text="Recent Operations",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=20
        )
        history_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(
            history_frame,
            height=10,
            font=("Courier", 10),
            state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        refresh_btn = tk.Button(
            history_frame,
            text="Refresh History",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            command=self.refresh_history
        )
        refresh_btn.pack(pady=10)
        
        # Load initial history
        self.refresh_history()
    
    def on_cancel_request(self):
        """Handle cancel request action"""
        request_id = self.request_id_entry.get().strip()
        
        if not request_id:
            messagebox.showerror("Error", "Please enter a Request ID")
            return
        
        # TODO: Call parking_system.cancel_request(request_id)
        messagebox.showinfo("Success", f"Request {request_id} cancelled")
        self.request_id_entry.delete(0, tk.END)
        self.refresh_history()
    
    def on_rollback(self):
        """Handle rollback action"""
        try:
            count = int(self.rollback_count_spinbox.get())
            if count < 1:
                raise ValueError("Count must be positive")
            
            # TODO: Call parking_system.rollback(count)
            messagebox.showinfo("Success", f"Rolled back {count} operation(s)")
            self.refresh_history()
        except ValueError as e:
            messagebox.showerror("Error", "Please enter a valid positive number")
    
    def refresh_history(self):
        """Refresh operation history"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        # TODO: Get actual history from parking_system
        placeholder = "Operation history will appear here...\n"
        self.history_text.insert(tk.END, placeholder)
        
        self.history_text.config(state=tk.DISABLED)
