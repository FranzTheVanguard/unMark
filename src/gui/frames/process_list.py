import tkinter as tk
from tkinter import ttk

class ProcessListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create treeview
        columns = ('Name', 'PID', 'Username', 'Memory')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        
        # Define headings with sort functionality
        for col in columns:
            self.tree.heading(col, text=col, 
                            command=lambda c=col: self.sort_column(c))
        
        # Define column widths
        self.tree.column('Name', width=200)
        self.tree.column('PID', width=100)
        self.tree.column('Username', width=150)
        self.tree.column('Memory', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Track sort order
        self.sort_reverse = False
        self.last_sorted_column = None
    
    def sort_column(self, column):
        """Sort tree contents when a column header is clicked"""
        # Get all items in the tree
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children('')]
        
        # If clicking the same column, reverse the sort
        if self.last_sorted_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
            self.last_sorted_column = column

        # Sort based on column type
        if column in ('PID', 'Memory'):
            # Numeric sort for PID and Memory
            # Convert memory string "1,234 K" to number for sorting
            if column == 'Memory':
                items.sort(key=lambda x: int(x[0].replace(',', '').split()[0]), 
                         reverse=self.sort_reverse)
            else:
                items.sort(key=lambda x: int(x[0]), reverse=self.sort_reverse)
        else:
            # Text sort for other columns
            items.sort(reverse=self.sort_reverse)

        # Rearrange items in sorted positions
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)
    
    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def update_table(self, processes):
        self.clear_table()
        for proc in processes:
            memory_kb = proc.info['memory_info'].rss // 1024
            self.tree.insert('', tk.END, values=(
                proc.info['name'],
                proc.info['pid'],
                proc.info['username'],
                f"{memory_kb:,} K"
            )) 