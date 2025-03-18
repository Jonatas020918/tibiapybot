import tkinter as tk
from tkinter import ttk, messagebox
import threading
from path_recorder import PathRecorder
import keyboard
import time

class PathRecorderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tibia Path Recorder")
        self.root.geometry("400x500")
        
        self.recorder = PathRecorder()
        self.recording_thread = None
        self.playing_thread = None
        
        self.setup_gui()
        self.setup_keyboard_listener()
        
    def setup_gui(self):
        """Setup the GUI elements"""
        # Status Frame
        status_frame = ttk.LabelFrame(self.root, text="Status", padding="5")
        status_frame.pack(fill="x", padx=5, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack()
        
        # Control Frame
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding="5")
        control_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(control_frame, text="Start Recording (F7)", 
                  command=self.start_recording).pack(fill="x", pady=2)
        ttk.Button(control_frame, text="Stop Recording (F8)", 
                  command=self.stop_recording).pack(fill="x", pady=2)
        
        # Paths Frame
        paths_frame = ttk.LabelFrame(self.root, text="Recorded Paths", padding="5")
        paths_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Paths List
        self.paths_listbox = tk.Listbox(paths_frame)
        self.paths_listbox.pack(fill="both", expand=True)
        
        # Path Control Frame
        path_control_frame = ttk.Frame(paths_frame)
        path_control_frame.pack(fill="x", pady=5)
        
        ttk.Button(path_control_frame, text="Play Selected", 
                  command=self.play_selected_path).pack(side="left", padx=2)
        ttk.Button(path_control_frame, text="Delete Selected", 
                  command=self.delete_selected_path).pack(side="left", padx=2)
        ttk.Button(path_control_frame, text="Refresh List", 
                  command=self.refresh_paths_list).pack(side="left", padx=2)
        
        # Hotkeys Frame
        hotkeys_frame = ttk.LabelFrame(self.root, text="Hotkeys", padding="5")
        hotkeys_frame.pack(fill="x", padx=5, pady=5)
        
        hotkeys_text = """
        F7 - Start Recording
        F8 - Stop Recording
        F9 - Stop Playback
        F10 - List Recorded Paths
        F11 - Play Last Recorded Path
        ESC - Exit
        """
        
        ttk.Label(hotkeys_frame, text=hotkeys_text, justify="left").pack()
        
    def setup_keyboard_listener(self):
        """Setup keyboard listener thread"""
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener, daemon=True)
        self.keyboard_thread.start()
        
    def keyboard_listener(self):
        """Listen for keyboard events"""
        while True:
            if keyboard.is_pressed('f7'):
                self.start_recording()
            elif keyboard.is_pressed('f8'):
                self.stop_recording()
            elif keyboard.is_pressed('f9'):
                self.stop_playback()
            elif keyboard.is_pressed('f10'):
                self.refresh_paths_list()
            elif keyboard.is_pressed('f11'):
                self.play_last_path()
            elif keyboard.is_pressed('esc'):
                self.root.quit()
            time.sleep(0.1)
            
    def start_recording(self):
        """Start recording a new path"""
        if not self.recorder.recording:
            self.status_label.config(text="Recording...")
            self.recording_thread = threading.Thread(target=self.recorder.start_recording)
            self.recording_thread.start()
            
    def stop_recording(self):
        """Stop recording the current path"""
        if self.recorder.recording:
            self.recorder.stop_recording()
            self.status_label.config(text="Recording stopped")
            self.refresh_paths_list()
            
    def stop_playback(self):
        """Stop playing the current path"""
        if self.recorder.playing:
            self.recorder.stop_playback()
            self.status_label.config(text="Playback stopped")
            
    def play_selected_path(self):
        """Play the selected path from the list"""
        selection = self.paths_listbox.curselection()
        if selection:
            filename = self.paths_listbox.get(selection[0])
            self.status_label.config(text=f"Playing: {filename}")
            self.playing_thread = threading.Thread(
                target=self.recorder.play_path, 
                args=(filename,)
            )
            self.playing_thread.start()
            
    def play_last_path(self):
        """Play the most recently recorded path"""
        paths = self.recorder.list_recorded_paths()
        if paths:
            filename = paths[-1]
            self.status_label.config(text=f"Playing: {filename}")
            self.playing_thread = threading.Thread(
                target=self.recorder.play_path, 
                args=(filename,)
            )
            self.playing_thread.start()
            
    def delete_selected_path(self):
        """Delete the selected path"""
        selection = self.paths_listbox.curselection()
        if selection:
            filename = self.paths_listbox.get(selection[0])
            if messagebox.askyesno("Confirm Delete", f"Delete {filename}?"):
                if self.recorder.delete_path(filename):
                    self.refresh_paths_list()
                    messagebox.showinfo("Success", "Path deleted successfully")
                else:
                    messagebox.showerror("Error", "Failed to delete path")
                    
    def refresh_paths_list(self):
        """Refresh the list of recorded paths"""
        self.paths_listbox.delete(0, tk.END)
        for path in self.recorder.list_recorded_paths():
            self.paths_listbox.insert(tk.END, path)
            
    def run(self):
        """Start the GUI"""
        self.refresh_paths_list()
        self.root.mainloop()

if __name__ == "__main__":
    app = PathRecorderGUI()
    app.run() 