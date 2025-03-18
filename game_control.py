import pyautogui
import keyboard
import mouse
import random
import time
import logging
from config import *

class GameControl:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pyautogui.FAILSAFE = True
        self.last_action_time = 0

    def random_delay(self):
        """Add random delay between actions"""
        if RANDOM_DELAYS:
            delay = random.uniform(0.5, 2.0)
            time.sleep(delay)

    def move_to(self, x, y, duration=None):
        """Move mouse to coordinates with optional human-like movement"""
        if HUMAN_LIKE_MOVEMENT:
            # Generate intermediate points for smooth movement
            current_x, current_y = pyautogui.position()
            steps = 10
            for i in range(steps):
                intermediate_x = current_x + (x - current_x) * (i + 1) / steps
                intermediate_y = current_y + (y - current_y) * (i + 1) / steps
                pyautogui.moveTo(intermediate_x, intermediate_y, duration=0.1)
                time.sleep(random.uniform(0.01, 0.03))
        else:
            pyautogui.moveTo(x, y, duration=duration)

    def click(self, x=None, y=None, button='left'):
        """Click at current position or specified coordinates"""
        if x is not None and y is not None:
            self.move_to(x, y)
        pyautogui.click(button=button)
        self.random_delay()

    def press_key(self, key):
        """Press a key"""
        keyboard.press_and_release(key)
        self.random_delay()

    def attack(self):
        """Perform attack action"""
        self.press_key(HOTKEYS["attack"])
        self.random_delay()

    def heal(self):
        """Use healing spell/potion"""
        self.press_key(HOTKEYS["heal"])
        self.random_delay()

    def use_mana_potion(self):
        """Use mana potion"""
        self.press_key(HOTKEYS["mana_potion"])
        self.random_delay()

    def loot(self):
        """Use loot action"""
        self.press_key(HOTKEYS["loot"])
        self.random_delay()

    def logout(self):
        """Perform logout action"""
        self.press_key(HOTKEYS["logout"])
        self.random_delay()

    def move_character(self, direction):
        """Move character in specified direction"""
        # Map directions to arrow keys
        direction_keys = {
            'up': 'up',
            'down': 'down',
            'left': 'left',
            'right': 'right'
        }
        
        if direction in direction_keys:
            self.press_key(direction_keys[direction])
            self.random_delay()

    def collect_loot(self, loot_location):
        """Move to and collect loot"""
        x, y = loot_location
        self.move_to(x, y)
        self.click()
        self.loot()
        self.random_delay()

    def emergency_heal(self):
        """Perform emergency healing"""
        self.heal()
        time.sleep(0.5)  # Wait for heal to take effect
        self.heal()  # Double heal for safety

    def check_emergency(self):
        """Check for emergency conditions"""
        if keyboard.is_pressed('esc'):  # Emergency stop
            self.logger.warning("Emergency stop triggered")
            return True
        return False 