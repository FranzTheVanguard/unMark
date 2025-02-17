import tkinter as tk
from tkinter import ttk

class CreateToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind('<Enter>', self.show_tooltip)
        self.widget.bind('<Leave>', self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip, text=self.text, 
                         background="#ffffe0", relief='solid', borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ControlsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create buttons
        self.check_btn = ttk.Button(self, text="Check")
        self.kill_btn = ttk.Button(self, text="Kill")
        self.start_btn = ttk.Button(self, text="Start")
        
        # Add tooltips
        CreateToolTip(self.check_btn, "Check for running target processes")
        CreateToolTip(self.kill_btn, "Terminate all target processes")
        CreateToolTip(self.start_btn, "Start all target services")
        
        # Layout
        self.check_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.kill_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5) 