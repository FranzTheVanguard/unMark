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
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Process')
        self.notebook.add(self.tab2, text='Word')
        
        # Add title to second tab
        title_label = ttk.Label(
            self.tab2,
            text="MarkAny Document SAFER Word Add In",
            font=('Segoe UI', '12', 'bold'),
            padding=10
        )
        title_label.pack(anchor='w', padx=10, pady=(10, 20))
        
        # Create frame for Word controls
        word_frame = ttk.Frame(self.tab2)
        word_frame.pack(fill='x', padx=10, pady=5)
        
        # Add system info to second tab
        system_info = ttk.Label(
            word_frame, 
            text=f"System Architecture: {self.process_handler.get_architecture()}",
            font=('Segoe UI', '10'),
            padding=(0, 5)
        )
        system_info.pack(anchor='w')
        
        # Add Word version label and combobox
        version_label = ttk.Label(
            word_frame,
            text="Select word version:",
            font=('Segoe UI', '10'),
            padding=(0, 15, 0, 5)
        )
        version_label.pack(anchor='w')
        
        self.word_versions = self.process_handler.word_versions
        self.word_combo = ttk.Combobox(
            word_frame, 
            values=self.word_versions,
            state='readonly',
            font=('Segoe UI', '10'),
            width=30
        )
        if self.word_versions:
            self.word_combo.set(self.word_versions[0])
        self.word_combo.pack(pady=(0, 5))
        
        # Add directory label
        dir_label = ttk.Label(
            word_frame,
            text="Select your Document SAFER folder:",
            font=('Segoe UI', '10'),
            padding=(0, 15, 0, 5)
        )
        dir_label.pack(anchor='w')
        
        # Create directory browser frame
        dir_frame = ttk.Frame(word_frame)
        dir_frame.pack(pady=5)
        
        # Add directory entry and browse button
        self.dir_entry = ttk.Entry(dir_frame, width=40, font=('Segoe UI', '10'))
        self.browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        
        self.dir_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.browse_btn.pack(side=tk.LEFT)
        
        # Create button frame
        button_frame = ttk.Frame(word_frame)
        button_frame.pack(pady=15)
        
        # Add control buttons
        self.disable_btn = ttk.Button(button_frame, text="Disable", command=self.disable_word)
        self.enable_btn = ttk.Button(button_frame, text="Enable", command=self.enable_word)
        
        self.disable_btn.pack(side=tk.LEFT, padx=2)
        self.enable_btn.pack(side=tk.LEFT, padx=2)
        
        # Create frames in first tab
        self.process_list = ProcessListFrame(self.tab1)
        self.controls = ControlsFrame(self.tab1)
        
        # Layout for first tab
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

    def disable_word(self):
        selected = self.word_combo.get()
        folder = self.dir_entry.get()
        
        if not selected:
            messagebox.showerror("Error", "Please select a Word version")
            return
        
        if not folder:
            messagebox.showerror("Error", "Please select the Document SAFER folder")
            return
        
        success, message = self.process_handler.toggle_dll(folder, selected, disable=True)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def enable_word(self):
        selected = self.word_combo.get()
        folder = self.dir_entry.get()
        
        if not selected:
            messagebox.showerror("Error", "Please select a Word version")
            return
        
        if not folder:
            messagebox.showerror("Error", "Please select the Document SAFER folder")
            return
        
        success, message = self.process_handler.toggle_dll(folder, selected, disable=False)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)