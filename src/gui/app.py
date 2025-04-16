import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .frames.process_list import ProcessListFrame
from .frames.controls import ControlsFrame
from ..core.process_handler import ProcessHandler
import os
import sys

class ProcessManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("unMark")
        self.geometry("600x400")
        
        # Set both window and taskbar icons
        try:
            # Get the correct path whether running as script or frozen executable
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running as script
                base_path = os.path.abspath(os.path.dirname(__file__))
                base_path = os.path.dirname(os.path.dirname(base_path))
                
            icon_path = os.path.join(base_path, 'unmark-ico.ico')
            self.iconbitmap(default=icon_path)
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to set icon: {e}")  # For debugging
        
        self.process_handler = ProcessHandler()
        
        # Style configuration for tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 5], font=('Segoe UI', '10'))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.tab1 = ttk.Frame(self.notebook) # Process Tab
        self.tab2 = ttk.Frame(self.notebook) # Word Tab
        self.tab3 = ttk.Frame(self.notebook) # Excel Tab
        
        self.notebook.add(self.tab1, text='Process')
        self.notebook.add(self.tab2, text='Word Add-in')
        self.notebook.add(self.tab3, text='Excel Add-in') # Add Excel tab
        
        # Add attribute to store the shared directory path
        self.shared_directory_path = tk.StringVar() 
        
        # --- Populate Process Tab (Tab 1) ---
        self.process_list = ProcessListFrame(self.tab1)
        self.controls = ControlsFrame(self.tab1)
        self.process_list.pack(expand=True, fill='both', padx=5, pady=5)
        self.controls.pack(fill='x', padx=5, pady=5)
        self.controls.check_btn.configure(command=self.check_processes)
        self.controls.kill_btn.configure(command=self.kill_processes)
        self.controls.start_btn.configure(command=self.start_services)
        
        # --- Populate Word Tab (Tab 2) ---
        self._populate_addin_tab(
            self.tab2, 
            "Word", 
            "MarkAny Document SAFER Word Add In"
        )

        # --- Populate Excel Tab (Tab 3) ---
        self._populate_addin_tab(
            self.tab3, 
            "Excel", 
            "MarkAny Document SAFER Excel Add In"
        )
    
    def _populate_addin_tab(self, tab_frame, app_type, title_text):
        """Helper method to populate Word/Excel tabs to avoid repetition."""
        
        # Add title
        title_label = ttk.Label(tab_frame, text=title_text, font=('Segoe UI', '12', 'bold'), padding=10)
        title_label.pack(anchor='w', padx=10, pady=(10, 20))
        
        # Frame for controls
        controls_frame = ttk.Frame(tab_frame)
        controls_frame.pack(fill='x', padx=10, pady=5)

        # System info
        system_info = ttk.Label(controls_frame, text=f"System Architecture: {self.process_handler.get_architecture()}", font=('Segoe UI', '10'), padding=(0, 5))
        system_info.pack(anchor='w')

        # Version selection
        version_label = ttk.Label(controls_frame, text=f"Select {app_type} version (Year):", font=('Segoe UI', '10'), padding=(0, 15, 0, 5))
        version_label.pack(anchor='w')
        
        combo = ttk.Combobox(controls_frame, values=self.process_handler.office_versions, state='readonly', font=('Segoe UI', '10'), width=30)
        if self.process_handler.office_versions:
            combo.set(self.process_handler.office_versions[-1]) # Default to latest
        combo.pack(pady=(0, 5))

        # Directory selection
        dir_label = ttk.Label(controls_frame, text="Select your Document SAFER folder:", font=('Segoe UI', '10'), padding=(0, 15, 0, 5))
        dir_label.pack(anchor='w')
        
        dir_frame = ttk.Frame(controls_frame)
        dir_frame.pack(pady=5)
        
        # Use the shared tk.StringVar for the directory entry
        dir_entry = ttk.Entry(dir_frame, width=40, font=('Segoe UI', '10'), 
                              textvariable=self.shared_directory_path) 
        # Update browse command to call the modified browse_directory
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory) 
        dir_entry.pack(side=tk.LEFT, padx=(0, 5))
        browse_btn.pack(side=tk.LEFT)

        # Enable/Disable buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(pady=15)
        
        # Use lambda to pass necessary info to the toggle function
        disable_btn = ttk.Button(button_frame, text="Disable", 
                                 command=lambda: self.toggle_addin(app_type, combo, dir_entry, disable=True))
        enable_btn = ttk.Button(button_frame, text="Enable", 
                                command=lambda: self.toggle_addin(app_type, combo, dir_entry, disable=False))
                                 
        disable_btn.pack(side=tk.LEFT, padx=2)
        enable_btn.pack(side=tk.LEFT, padx=2)

        # Store references (this part is actually not needed for synchronization anymore,
        # but keep it if you might need direct access to widgets later)
        setattr(self, f"{app_type.lower()}_combo", combo)
        setattr(self, f"{app_type.lower()}_dir_entry", dir_entry) # Keep for toggle_addin

    def toggle_addin(self, app_type, combo_widget, dir_entry_widget, disable):
        """Generic method to handle enabling/disabling add-ins."""
        selected_year = combo_widget.get()
        # Get folder path from the shared variable, not the specific widget's content
        folder = self.shared_directory_path.get() 
        action = "disable" if disable else "enable"

        if not selected_year:
            messagebox.showerror("Error", f"Please select an {app_type} version (Year)")
            return
        
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid Document SAFER folder")
            return
        
        success, message = self.process_handler.toggle_add_in(
            app_type, folder, selected_year, disable=disable
        )
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror(f"{action.capitalize()} Error", message)

    def check_processes(self):
        processes = self.process_handler.find_processes()
        self.process_list.update_table(processes)
        if not processes:
            messagebox.showinfo("Info", "No target processes found")
    
    def kill_processes(self):
        results = self.process_handler.terminate_processes()
        if results:
            message = "\n".join([f"{name}: {status}" for name, status in results])
            messagebox.showinfo("Termination Results", message)
        else:
            messagebox.showinfo("Info", "No processes to terminate")

    def start_services(self):
        try:
            results = self.process_handler.start_services()
            message = "\n".join([f"{name}: {status}" for name, status in results])
            messagebox.showinfo("Service Start Results", message)
            # Refresh the process list after starting services
            self.check_processes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start services: {str(e)}")

    def browse_directory(self):
        """Handles directory browsing and updates the shared path variable."""
        # Suggest the current path as starting directory if one exists
        initial_dir = self.shared_directory_path.get() or "/" 
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            # Update the shared tk.StringVar, which automatically updates all linked Entry widgets
            self.shared_directory_path.set(directory) 