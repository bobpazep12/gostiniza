import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta

class HotelApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#333333",
                "frame_bg": "#ffffff",
                "frame_fg": "#333333",
                "button_bg": "#4CAF50",
                "button_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "entry_fg": "#333333",
                "tree_bg": "#ffffff",
                "tree_fg": "#333333",
                "tree_selected": "#4CAF50",
                "title_bg": "#2c3e50",
                "title_fg": "#ffffff"
            },
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "frame_bg": "#2d2d2d",
                "frame_fg": "#ffffff",
                "button_bg": "#3498db",
                "button_fg": "#ffffff",
                "entry_bg": "#3d3d3d",
                "entry_fg": "#ffffff",
                "tree_bg": "#2d2d2d",
                "tree_fg": "#ffffff",
                "tree_selected": "#3498db",
                "title_bg": "#000000",
                "title_fg": "#ffffff"
            }
        }
        self.setup_main_window()
        self.create_menu()
        self.create_dashboard()
        self.apply_theme()
    
    def setup_main_window(self):
        self.root.title("Hotel Management System - Guest House")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
    
    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=theme["tree_bg"], foreground=theme["tree_fg"], fieldbackground=theme["tree_bg"])
        style.map("Treeview", background=[("selected", theme["tree_selected"])])
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Backup Database", command=self.backup_db)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Light", command=lambda: self.switch_theme("light"))
        theme_menu.add_command(label="Dark", command=lambda: self.switch_theme("dark"))
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def switch_theme(self, theme):
        self.current_theme = theme
        self.apply_theme()
        self.refresh_ui()
    
    def refresh_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_menu()
        self.create_dashboard()
    
    def create_dashboard(self):
        theme = self.themes[self.current_theme]
        
        header = tk.Frame(self.root, bg=theme["title_bg"], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="HOTEL MANAGEMENT SYSTEM", 
                         font=("Arial", 18, "bold"), 
                         bg=theme["title_bg"], fg=theme["title_fg"])
        title.pack(expand=True)
        
        main_frame = tk.Frame(self.root, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(main_frame, bg=theme["bg"], width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        buttons = [
            ("Rooms", self.open_rooms),
            (
