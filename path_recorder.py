import keyboard
import mouse
import time
import json
import os
from datetime import datetime
import logging
from game_control import GameControl

class PathRecorder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.game_control = GameControl()
        self.recording = False
        self.playing = False
        self.path_data = []
        self.current_path = None
        self.paths_directory = "recorded_paths"
        
        # Create directory for recorded paths if it doesn't exist
        if not os.path.exists(self.paths_directory):
            os.makedirs(self.paths_directory)

    def start_recording(self):
        """Start recording the path"""
        self.recording = True
        self.path_data = []
        self.logger.info("Started recording path. Press 'F8' to stop recording.")
        
        # Record initial position
        initial_pos = mouse.get_position()
        self.path_data.append({
            "type": "position",
            "x": initial_pos[0],
            "y": initial_pos[1],
            "timestamp": time.time()
        })

        try:
            while self.recording:
                if keyboard.is_pressed('f8'):  # Stop recording
                    self.stop_recording()
                    break

                # Record mouse position
                current_pos = mouse.get_position()
                self.path_data.append({
                    "type": "position",
                    "x": current_pos[0],
                    "y": current_pos[1],
                    "timestamp": time.time()
                })

                # Record mouse clicks
                if mouse.is_pressed(button='left'):
                    self.path_data.append({
                        "type": "click",
                        "button": "left",
                        "timestamp": time.time()
                    })

                # Record keyboard presses
                for key in ['up', 'down', 'left', 'right']:
                    if keyboard.is_pressed(key):
                        self.path_data.append({
                            "type": "keypress",
                            "key": key,
                            "timestamp": time.time()
                        })

                time.sleep(0.1)  # Reduce CPU usage

        except Exception as e:
            self.logger.error(f"Error during recording: {e}")
            self.stop_recording()

    def stop_recording(self):
        """Stop recording and save the path"""
        self.recording = False
        if self.path_data:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"path_{timestamp}.json"
            filepath = os.path.join(self.paths_directory, filename)

            # Save path data
            with open(filepath, 'w') as f:
                json.dump(self.path_data, f, indent=4)

            self.logger.info(f"Path saved to {filepath}")
            return filename
        return None

    def load_path(self, filename):
        """Load a recorded path from file"""
        filepath = os.path.join(self.paths_directory, filename)
        try:
            with open(filepath, 'r') as f:
                self.path_data = json.load(f)
            self.logger.info(f"Loaded path from {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error loading path: {e}")
            return False

    def play_path(self, filename=None):
        """Play back a recorded path"""
        if filename and not self.load_path(filename):
            return False

        if not self.path_data:
            self.logger.error("No path data to play")
            return False

        self.playing = True
        self.logger.info("Starting path playback. Press 'F9' to stop.")

        try:
            start_time = time.time()
            for action in self.path_data:
                if not self.playing:
                    break

                if keyboard.is_pressed('f9'):  # Emergency stop
                    self.stop_playback()
                    break

                # Calculate delay based on timestamps
                if action != self.path_data[0]:  # Skip first action
                    delay = action["timestamp"] - self.path_data[self.path_data.index(action) - 1]["timestamp"]
                    time.sleep(delay)

                # Execute action
                if action["type"] == "position":
                    self.game_control.move_to(action["x"], action["y"])
                elif action["type"] == "click":
                    self.game_control.click(button=action["button"])
                elif action["type"] == "keypress":
                    self.game_control.move_character(action["key"])

        except Exception as e:
            self.logger.error(f"Error during playback: {e}")
        finally:
            self.stop_playback()

    def stop_playback(self):
        """Stop playing the recorded path"""
        self.playing = False
        self.logger.info("Stopped path playback")

    def list_recorded_paths(self):
        """List all recorded paths"""
        try:
            paths = os.listdir(self.paths_directory)
            return [path for path in paths if path.endswith('.json')]
        except Exception as e:
            self.logger.error(f"Error listing paths: {e}")
            return []

    def delete_path(self, filename):
        """Delete a recorded path"""
        filepath = os.path.join(self.paths_directory, filename)
        try:
            os.remove(filepath)
            self.logger.info(f"Deleted path: {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting path: {e}")
            return False

def main():
    """Test the path recorder"""
    recorder = PathRecorder()
    
    print("Path Recorder Commands:")
    print("F7 - Start Recording")
    print("F8 - Stop Recording")
    print("F9 - Stop Playback")
    print("F10 - List Recorded Paths")
    print("F11 - Play Last Recorded Path")
    print("ESC - Exit")

    while True:
        if keyboard.is_pressed('f7'):
            recorder.start_recording()
        elif keyboard.is_pressed('f10'):
            paths = recorder.list_recorded_paths()
            print("\nRecorded Paths:")
            for path in paths:
                print(f"- {path}")
        elif keyboard.is_pressed('f11'):
            paths = recorder.list_recorded_paths()
            if paths:
                recorder.play_path(paths[-1])  # Play the most recent path
        elif keyboard.is_pressed('esc'):
            break

        time.sleep(0.1)

if __name__ == "__main__":
    main() 