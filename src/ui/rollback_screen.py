"""
Rollback Screen
Handles cancellation and rollback operations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from enums import RequestState


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
            text="Rollback Operations",
            font=("Arial", 20, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # Info section
        info_frame = tk.Frame(self, bg="#ecf0f1", relief=tk.RIDGE, borderwidth=2)
        info_frame.pack(pady=10, padx=50, fill=tk.X)
        
        info_text = tk.Label(
            info_frame,
            text="ℹ️  Rollback uses STACK (LIFO) data structure to undo operations\n"
                 "The most recent operations are undone first",
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#2c3e50",
            justify=tk.LEFT,
            padx=20,
            pady=15
        )
        info_text.pack()
        
        # Rollback Section
        rollback_frame = tk.LabelFrame(
            self,
            text="Rollback Operations",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=20
        )
        rollback_frame.pack(pady=20, padx=50, fill=tk.X)
        
        # Info row
        info_row = tk.Frame(rollback_frame)
        info_row.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky=tk.W)
        
        tk.Label(
            info_row,
            text="Operations in history:",
            font=("Arial", 11)
        ).pack(side=tk.LEFT)
        
        self.operation_count_label = tk.Label(
            info_row,
            text="0",
            font=("Arial", 11, "bold"),
            fg="#3498db"
        )
        self.operation_count_label.pack(side=tk.LEFT, padx=5)
        
        tk.Label(rollback_frame, text="Number of Operations:", font=("Arial", 12)).grid(
            row=1, column=0, sticky=tk.W, pady=10
        )
        self.rollback_count_spinbox = tk.Spinbox(
            rollback_frame,
            from_=1,
            to=100,
            font=("Arial", 12),
            width=18
        )
        self.rollback_count_spinbox.grid(row=1, column=1, pady=10, padx=10)
        
        rollback_btn = tk.Button(
            rollback_frame,
            text="Rollback",
            font=("Arial", 12),
            bg="#f39c12",
            fg="white",
            command=self.on_rollback
        )
        rollback_btn.grid(row=1, column=2, pady=10, padx=10)
        
        # Warning label
        warning_label = tk.Label(
            rollback_frame,
            text="⚠️ Warning: Rollback will undo the last N operations (LIFO order)",
            font=("Arial", 9),
            fg="#e67e22"
        )
        warning_label.grid(row=2, column=0, columnspan=3, pady=(0, 5))
        
        # Operation History
        history_frame = tk.LabelFrame(
            self,
            text="Recent Operations",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=20
        )
        history_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to history text
        history_scroll_frame = tk.Frame(history_frame)
        history_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(history_scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(
            history_scroll_frame,
            height=10,
            font=("Courier", 10),
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set
        )
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        refresh_btn = tk.Button(
            history_frame,
            text="Refresh History",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            command=self.refresh_history
        )
        refresh_btn.pack(pady=10)
        
        # Load initial data
        self.refresh_history()
    
    def on_tab_selected(self):
        """Called when this tab is selected - refresh data"""
        self.refresh_history()
    
    # ========== ROLLBACK OPERATIONS ==========
    
    def on_rollback(self):
        """Called when this tab is selected - refresh data"""
        self.load_cancellable_requests()
        self.refresh_history()
    
    # ========== ROLLBACK OPERATIONS ==========
    
    def on_rollback(self):
        """Handle rollback action"""
        try:
            count = int(self.rollback_count_spinbox.get())
            if count < 1:
                raise ValueError("Count must be positive")
            
            # Check operation count
            operation_count = self.parking_system.rollback_manager.get_operation_count()
            
            if operation_count == 0:
                messagebox.showinfo(
                    "No Operations",
                    "There are no operations in history to rollback."
                )
                return
            
            if count > operation_count:
                messagebox.showwarning(
                    "Too Many Operations",
                    f"Cannot rollback {count} operations.\n"
                    f"Only {operation_count} operations in history.\n\n"
                    f"Rollback will undo all {operation_count} operations."
                )
                count = operation_count
            
            # Show preview of what will be rolled back
            preview_msg = f"Rollback the last {count} operation(s)?\n\n"
            preview_msg += "This will undo the following (in LIFO order):\n"
            
            # Get last N operations for preview
            stack = self.parking_system.rollback_manager.operation_stack
            preview_count = min(count, 5)  # Show max 5 operations
            for i in range(1, preview_count + 1):
                if len(stack) >= i:
                    op = stack[-i]
                    preview_msg += f"{i}. {op.operation_type} - Request: {op.request_id}\n"
            
            if count > 5:
                preview_msg += f"... and {count - 5} more operation(s)\n"
            
            preview_msg += "\n⚠️ This action cannot be undone!"
            
            # Confirm action
            confirm = messagebox.askyesno(
                "Confirm Rollback",
                preview_msg
            )
            
            if not confirm:
                return
            
            # Call parking system rollback method
            result = self.parking_system.rollback_operations(count)
            
            if result['success']:
                message = result['message']
                if 'operations_rolled_back' in result:
                    message += f"\n\nOperations rolled back: {result['operations_rolled_back']}"
                
                messagebox.showinfo("Success", message)
                self.refresh_history()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number")
        except Exception as e:
            print(f"Error during rollback: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to rollback: {str(e)}")
    
    def refresh_history(self):
        """Refresh operation history from rollback manager"""
        try:
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            
            # Get operation count
            operation_count = self.parking_system.rollback_manager.get_operation_count()
            self.operation_count_label.config(text=str(operation_count))
            
            if operation_count == 0:
                self.history_text.insert(tk.END, "No operations in history yet.\n\n")
                self.history_text.insert(tk.END, "Operations are recorded when you:\n")
                self.history_text.insert(tk.END, "- Allocate parking\n")
                self.history_text.insert(tk.END, "- Cancel requests\n")
                self.history_text.insert(tk.END, "- Release parking\n")
            else:
                # Display operations in LIFO order (most recent first)
                self.history_text.insert(tk.END, f"Operation History (Total: {operation_count})\n")
                self.history_text.insert(tk.END, "="*60 + "\n")
                self.history_text.insert(tk.END, "Stack Order: Most Recent → Oldest (LIFO)\n")
                self.history_text.insert(tk.END, "="*60 + "\n\n")
                
                stack = self.parking_system.rollback_manager.operation_stack
                
                # Show last 20 operations
                display_count = min(20, len(stack))
                
                for i in range(display_count):
                    op = stack[-(i+1)]  # Get from top of stack
                    
                    self.history_text.insert(tk.END, f"[{i+1}] Operation Type: {op.operation_type}\n")
                    self.history_text.insert(tk.END, f"    Request ID: {op.request_id}\n")
                    self.history_text.insert(tk.END, f"    Slot ID: {op.slot_id}\n")
                    self.history_text.insert(tk.END, f"    Previous State: {op.request_previous_state.value if op.request_previous_state else 'N/A'}\n")
                    
                    if op.request_previous_allocated_slot:
                        self.history_text.insert(tk.END, f"    Previous Slot: {op.request_previous_allocated_slot}\n")
                    
                    self.history_text.insert(tk.END, "\n")
                
                if operation_count > 20:
                    self.history_text.insert(tk.END, f"\n... and {operation_count - 20} more operations\n")
            
            self.history_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Error refreshing history: {e}")
            import traceback
            traceback.print_exc()
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            self.history_text.insert(tk.END, f"Error loading history: {str(e)}\n")
            self.history_text.config(state=tk.DISABLED)
    
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
