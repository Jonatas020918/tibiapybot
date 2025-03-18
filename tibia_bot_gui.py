import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from path_recorder import PathRecorder
from monsters import MONSTERS, get_monster_info
from hunting_spots import HUNTING_SPOTS, get_hunting_spot_info
import logging

class TibiaBotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tibia Bot")
        self.root.geometry("800x600")
        
        self.recorder = PathRecorder()
        self.settings = self.load_settings()
        
        self.setup_gui()
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging to GUI"""
        self.log_text = scrolledtext.ScrolledText(self.root, height=10)
        self.log_text.pack(fill="x", padx=5, pady=5)
        
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
                
            def emit(self, record):
                msg = self.format(record)
                def append():
                    self.text_widget.configure(state='normal')
                    self.text_widget.insert(tk.END, msg + '\n')
                    self.text_widget.configure(state='disabled')
                    self.text_widget.see(tk.END)
                self.text_widget.after(0, append)
        
        handler = GUILogHandler(self.log_text)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(handler)
        
    def setup_gui(self):
        """Setup the main GUI elements"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create tabs
        self.setup_general_tab()
        self.setup_hunting_tab()
        self.setup_potions_tab()
        self.setup_backpacks_tab()
        self.setup_paths_tab()
        self.setup_safety_tab()
        
    def setup_general_tab(self):
        """Setup the general settings tab"""
        general_frame = ttk.Frame(self.notebook)
        self.notebook.add(general_frame, text="General")
        
        # Character Settings
        char_frame = ttk.LabelFrame(general_frame, text="Character Settings", padding="5")
        char_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(char_frame, text="Character Name:").grid(row=0, column=0, padx=5, pady=2)
        self.char_name = ttk.Entry(char_frame)
        self.char_name.grid(row=0, column=1, padx=5, pady=2)
        self.char_name.insert(0, self.settings.get("character_name", ""))
        
        ttk.Label(char_frame, text="World:").grid(row=1, column=0, padx=5, pady=2)
        self.world = ttk.Entry(char_frame)
        self.world.grid(row=1, column=1, padx=5, pady=2)
        self.world.insert(0, self.settings.get("world", ""))
        
        # Game Window Settings
        window_frame = ttk.LabelFrame(general_frame, text="Game Window", padding="5")
        window_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(window_frame, text="Window Title:").grid(row=0, column=0, padx=5, pady=2)
        self.window_title = ttk.Entry(window_frame)
        self.window_title.grid(row=0, column=1, padx=5, pady=2)
        self.window_title.insert(0, self.settings.get("window_title", "Tibia"))
        
        # Save Button
        ttk.Button(general_frame, text="Save Settings", 
                  command=self.save_general_settings).pack(pady=10)
        
    def setup_hunting_tab(self):
        """Setup the hunting settings tab"""
        hunting_frame = ttk.Frame(self.notebook)
        self.notebook.add(hunting_frame, text="Hunting")
        
        # Hunting Spot Selection
        spot_frame = ttk.LabelFrame(hunting_frame, text="Hunting Spots", padding="5")
        spot_frame.pack(fill="x", padx=5, pady=5)
        
        self.spot_var = tk.StringVar()
        self.spot_combo = ttk.Combobox(spot_frame, textvariable=self.spot_var)
        self.spot_combo['values'] = self.get_all_hunting_spots()
        self.spot_combo.pack(fill="x", padx=5, pady=2)
        self.spot_combo.set(self.settings.get("current_spot", ""))
        
        # Monster Selection
        monster_frame = ttk.LabelFrame(hunting_frame, text="Target Monsters", padding="5")
        monster_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.monster_listbox = tk.Listbox(monster_frame, selectmode=tk.MULTIPLE)
        self.monster_listbox.pack(fill="both", expand=True, padx=5, pady=2)
        self.update_monster_list()
        
        # Save Button
        ttk.Button(hunting_frame, text="Save Hunting Settings", 
                  command=self.save_hunting_settings).pack(pady=10)
        
    def setup_potions_tab(self):
        """Setup the potions settings tab"""
        potions_frame = ttk.Frame(self.notebook)
        self.notebook.add(potions_frame, text="Potions")
        
        # Health Potion Settings
        hp_frame = ttk.LabelFrame(potions_frame, text="Health Potions", padding="5")
        hp_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(hp_frame, text="Hotkey:").grid(row=0, column=0, padx=5, pady=2)
        self.hp_hotkey = ttk.Entry(hp_frame)
        self.hp_hotkey.grid(row=0, column=1, padx=5, pady=2)
        self.hp_hotkey.insert(0, self.settings.get("hp_hotkey", "f1"))
        
        ttk.Label(hp_frame, text="Min HP %:").grid(row=1, column=0, padx=5, pady=2)
        self.min_hp = ttk.Entry(hp_frame)
        self.min_hp.grid(row=1, column=1, padx=5, pady=2)
        self.min_hp.insert(0, self.settings.get("min_hp", "70"))
        
        # Mana Potion Settings
        mp_frame = ttk.LabelFrame(potions_frame, text="Mana Potions", padding="5")
        mp_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(mp_frame, text="Hotkey:").grid(row=0, column=0, padx=5, pady=2)
        self.mp_hotkey = ttk.Entry(mp_frame)
        self.mp_hotkey.grid(row=0, column=1, padx=5, pady=2)
        self.mp_hotkey.insert(0, self.settings.get("mp_hotkey", "f2"))
        
        ttk.Label(mp_frame, text="Min MP %:").grid(row=1, column=0, padx=5, pady=2)
        self.min_mp = ttk.Entry(mp_frame)
        self.min_mp.grid(row=1, column=1, padx=5, pady=2)
        self.min_mp.insert(0, self.settings.get("min_mp", "30"))
        
        # Save Button
        ttk.Button(potions_frame, text="Save Potion Settings", 
                  command=self.save_potion_settings).pack(pady=10)
        
    def setup_backpacks_tab(self):
        """Setup the backpacks settings tab"""
        backpacks_frame = ttk.Frame(self.notebook)
        self.notebook.add(backpacks_frame, text="Backpacks")
        
        # Main Backpack
        main_frame = ttk.LabelFrame(backpacks_frame, text="Main Backpack", padding="5")
        main_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(main_frame, text="Hotkey:").grid(row=0, column=0, padx=5, pady=2)
        self.main_bp_hotkey = ttk.Entry(main_frame)
        self.main_bp_hotkey.grid(row=0, column=1, padx=5, pady=2)
        self.main_bp_hotkey.insert(0, self.settings.get("main_bp_hotkey", "f3"))
        
        # Loot Backpack
        loot_frame = ttk.LabelFrame(backpacks_frame, text="Loot Backpack", padding="5")
        loot_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(loot_frame, text="Hotkey:").grid(row=0, column=0, padx=5, pady=2)
        self.loot_bp_hotkey = ttk.Entry(loot_frame)
        self.loot_bp_hotkey.grid(row=0, column=1, padx=5, pady=2)
        self.loot_bp_hotkey.insert(0, self.settings.get("loot_bp_hotkey", "f4"))
        
        # Save Button
        ttk.Button(backpacks_frame, text="Save Backpack Settings", 
                  command=self.save_backpack_settings).pack(pady=10)
        
    def setup_paths_tab(self):
        """Setup the paths tab"""
        paths_frame = ttk.Frame(self.notebook)
        self.notebook.add(paths_frame, text="Paths")
        
        # Paths List
        list_frame = ttk.LabelFrame(paths_frame, text="Recorded Paths", padding="5")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.paths_listbox = tk.Listbox(list_frame)
        self.paths_listbox.pack(fill="both", expand=True, padx=5, pady=2)
        self.refresh_paths_list()
        
        # Path Controls
        control_frame = ttk.Frame(paths_frame)
        control_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(control_frame, text="Record New Path", 
                  command=self.start_recording).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Play Selected", 
                  command=self.play_selected_path).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Delete Selected", 
                  command=self.delete_selected_path).pack(side="left", padx=2)
        
    def setup_safety_tab(self):
        """Setup the safety settings tab"""
        safety_frame = ttk.Frame(self.notebook)
        self.notebook.add(safety_frame, text="Safety")
        
        # Emergency Settings
        emergency_frame = ttk.LabelFrame(safety_frame, text="Emergency Settings", padding="5")
        emergency_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(emergency_frame, text="Emergency HP %:").grid(row=0, column=0, padx=5, pady=2)
        self.emergency_hp = ttk.Entry(emergency_frame)
        self.emergency_hp.grid(row=0, column=1, padx=5, pady=2)
        self.emergency_hp.insert(0, self.settings.get("emergency_hp", "40"))
        
        ttk.Label(emergency_frame, text="Emergency Hotkey:").grid(row=1, column=0, padx=5, pady=2)
        self.emergency_hotkey = ttk.Entry(emergency_frame)
        self.emergency_hotkey.grid(row=1, column=1, padx=5, pady=2)
        self.emergency_hotkey.insert(0, self.settings.get("emergency_hotkey", "f9"))
        
        # Player Detection
        player_frame = ttk.LabelFrame(safety_frame, text="Player Detection", padding="5")
        player_frame.pack(fill="x", padx=5, pady=5)
        
        self.player_detection = tk.BooleanVar(value=self.settings.get("player_detection", True))
        ttk.Checkbutton(player_frame, text="Enable Player Detection", 
                       variable=self.player_detection).pack(padx=5, pady=2)
        
        # Save Button
        ttk.Button(safety_frame, text="Save Safety Settings", 
                  command=self.save_safety_settings).pack(pady=10)
        
    def load_settings(self):
        """Load settings from file"""
        try:
            with open("bot_settings.json", "r") as f:
                return json.load(f)
        except:
            return {}
            
    def save_settings(self):
        """Save all settings to file"""
        settings = {
            "character_name": self.char_name.get(),
            "world": self.world.get(),
            "window_title": self.window_title.get(),
            "current_spot": self.spot_var.get(),
            "target_monsters": [self.monster_listbox.get(i) for i in self.monster_listbox.curselection()],
            "hp_hotkey": self.hp_hotkey.get(),
            "min_hp": self.min_hp.get(),
            "mp_hotkey": self.mp_hotkey.get(),
            "min_mp": self.min_mp.get(),
            "main_bp_hotkey": self.main_bp_hotkey.get(),
            "loot_bp_hotkey": self.loot_bp_hotkey.get(),
            "emergency_hp": self.emergency_hp.get(),
            "emergency_hotkey": self.emergency_hotkey.get(),
            "player_detection": self.player_detection.get()
        }
        
        with open("bot_settings.json", "w") as f:
            json.dump(settings, f, indent=4)
            
    def get_all_hunting_spots(self):
        """Get list of all hunting spots"""
        spots = []
        for category in HUNTING_SPOTS.values():
            spots.extend(category.keys())
        return spots
        
    def update_monster_list(self):
        """Update the monster list based on selected hunting spot"""
        self.monster_listbox.delete(0, tk.END)
        spot_info = get_hunting_spot_info(self.spot_var.get())
        if spot_info:
            for monster in spot_info["monsters"]:
                self.monster_listbox.insert(tk.END, monster)
                
    def refresh_paths_list(self):
        """Refresh the list of recorded paths"""
        self.paths_listbox.delete(0, tk.END)
        for path in self.recorder.list_recorded_paths():
            self.paths_listbox.insert(tk.END, path)
            
    def start_recording(self):
        """Start recording a new path"""
        self.recorder.start_recording()
        
    def play_selected_path(self):
        """Play the selected path"""
        selection = self.paths_listbox.curselection()
        if selection:
            filename = self.paths_listbox.get(selection[0])
            self.recorder.play_path(filename)
            
    def delete_selected_path(self):
        """Delete the selected path"""
        selection = self.paths_listbox.curselection()
        if selection:
            filename = self.paths_listbox.get(selection[0])
            if messagebox.askyesno("Confirm Delete", f"Delete {filename}?"):
                self.recorder.delete_path(filename)
                self.refresh_paths_list()
                
    def save_general_settings(self):
        """Save general settings"""
        self.save_settings()
        messagebox.showinfo("Success", "General settings saved!")
        
    def save_hunting_settings(self):
        """Save hunting settings"""
        self.save_settings()
        messagebox.showinfo("Success", "Hunting settings saved!")
        
    def save_potion_settings(self):
        """Save potion settings"""
        self.save_settings()
        messagebox.showinfo("Success", "Potion settings saved!")
        
    def save_backpack_settings(self):
        """Save backpack settings"""
        self.save_settings()
        messagebox.showinfo("Success", "Backpack settings saved!")
        
    def save_safety_settings(self):
        """Save safety settings"""
        self.save_settings()
        messagebox.showinfo("Success", "Safety settings saved!")
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TibiaBotGUI()
    app.run() 