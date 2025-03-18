import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
import logging
from config import *

class ScreenRecognition:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.screenshot_region = None
        self.templates = {}
        self.load_templates()

    def load_templates(self):
        """Load template images for various game elements"""
        template_dir = "templates"
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
            self.logger.warning(f"Template directory created at {template_dir}")
            return

        for template_file in os.listdir(template_dir):
            if template_file.endswith(('.png', '.jpg')):
                template_name = os.path.splitext(template_file)[0]
                template_path = os.path.join(template_dir, template_file)
                self.templates[template_name] = cv2.imread(template_path)

    def capture_game_window(self):
        """Capture the game window"""
        try:
            window = pyautogui.getWindowsWithTitle(GAME_WINDOW_TITLE)
            if not window:
                self.logger.error("Tibia window not found")
                return None

            window = window[0]
            if not self.screenshot_region:
                self.screenshot_region = (
                    window.left,
                    window.top,
                    window.width,
                    window.height
                )

            screenshot = pyautogui.screenshot(region=self.screenshot_region)
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        except Exception as e:
            self.logger.error(f"Error capturing game window: {e}")
            return None

    def find_template(self, image, template_name, threshold=TEMPLATE_MATCHING_THRESHOLD):
        """Find a template in the image"""
        if template_name not in self.templates:
            self.logger.error(f"Template {template_name} not found")
            return None

        template = self.templates[template_name]
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)

        if len(locations[0]) == 0:
            return None

        # Return the first match
        return (locations[1][0], locations[0][0])

    def detect_text(self, image, region=None):
        """Detect text in a specific region of the image"""
        try:
            if region:
                x, y, w, h = region
                roi = image[y:y+h, x:x+w]
            else:
                roi = image

            text = pytesseract.image_to_string(roi)
            return text.strip()
        except Exception as e:
            self.logger.error(f"Error detecting text: {e}")
            return None

    def detect_hp_mp(self, image):
        """Detect HP and MP values from the game interface"""
        # These regions need to be configured based on your game window
        hp_region = (100, 50, 100, 20)  # Example coordinates
        mp_region = (100, 70, 100, 20)  # Example coordinates

        hp_text = self.detect_text(image, hp_region)
        mp_text = self.detect_text(image, mp_region)

        try:
            hp = int(hp_text.split('/')[0])
            mp = int(mp_text.split('/')[0])
            return hp, mp
        except:
            return None, None

    def detect_monster(self, image):
        """Detect monsters in the game window"""
        # This will need to be implemented based on your specific monster templates
        for monster in HUNTING_SPOTS[0]["monsters"]:
            location = self.find_template(image, monster)
            if location:
                return monster, location
        return None, None

    def detect_loot(self, image):
        """Detect loot items in the game window"""
        detected_loot = []
        for item in HUNTING_SPOTS[0]["loot_items"]:
            location = self.find_template(image, item)
            if location:
                detected_loot.append((item, location))
        return detected_loot

    def detect_player(self, image):
        """Detect other players in the game window"""
        # This will need to be implemented based on your specific player detection method
        # For example, looking for specific colors or patterns that indicate players
        return False  # Placeholder 