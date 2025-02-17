import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        
        # Create frames
        self.process_list = ProcessListFrame(self)
        self.controls = ControlsFrame(self)
        
        # Layout
        self.process_list.pack(expand=True, fill='both', padx=5, pady=5)
        self.controls.pack(fill='x', padx=5, pady=5)
        
        # Bind button actions
        self.controls.check_btn.configure(command=self.check_processes)
        self.controls.kill_btn.configure(command=self.kill_processes)
        self.controls.start_btn.configure(command=self.start_services)
    
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