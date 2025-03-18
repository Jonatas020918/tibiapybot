import logging
import time
from screen_recognition import ScreenRecognition
from game_control import GameControl
from config import *

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class TibiaBot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.screen_recognition = ScreenRecognition()
        self.game_control = GameControl()
        self.running = False
        self.current_hp = 0
        self.current_mp = 0
        self.last_action_time = 0

    def start(self):
        """Start the bot"""
        self.logger.info("Starting Tibia Bot...")
        self.running = True

        try:
            while self.running:
                # Check for emergency conditions
                if self.game_control.check_emergency():
                    self.logger.warning("Emergency stop triggered")
                    break

                # Capture game window
                game_image = self.screen_recognition.capture_game_window()
                if game_image is None:
                    self.logger.error("Failed to capture game window")
                    time.sleep(1)
                    continue

                # Check character status
                self.check_character_status(game_image)

                # Main bot loop
                self.bot_loop(game_image)

                # Small delay to prevent CPU overuse
                time.sleep(0.1)

        except Exception as e:
            self.logger.error(f"Bot error: {e}")
        finally:
            self.stop()

    def check_character_status(self, game_image):
        """Check and handle character status"""
        hp, mp = self.screen_recognition.detect_hp_mp(game_image)
        if hp is not None and mp is not None:
            self.current_hp = hp
            self.current_mp = mp

            # Emergency healing
            if self.current_hp < EMERGENCY_HP_PERCENT:
                self.logger.warning("Emergency healing triggered")
                self.game_control.emergency_heal()

            # Regular healing
            elif self.current_hp < MIN_HP_PERCENT:
                self.game_control.heal()

            # Mana potion
            if self.current_mp < MIN_MP_PERCENT:
                self.game_control.use_mana_potion()

    def bot_loop(self, game_image):
        """Main bot loop for hunting and looting"""
        # Check for players if enabled
        if PLAYER_DETECTION_ENABLED and self.screen_recognition.detect_player(game_image):
            self.logger.warning("Player detected, moving to safe spot")
            self.move_to_safe_spot()
            return

        # Look for monsters
        monster, monster_location = self.screen_recognition.detect_monster(game_image)
        if monster:
            self.logger.info(f"Found monster: {monster}")
            self.attack_monster(monster_location)

        # Look for loot
        loot_items = self.screen_recognition.detect_loot(game_image)
        for item, location in loot_items:
            self.logger.info(f"Found loot: {item}")
            self.game_control.collect_loot(location)

    def attack_monster(self, monster_location):
        """Handle monster attack sequence"""
        # Move to monster
        self.game_control.move_to(monster_location[0], monster_location[1])
        self.game_control.click()

        # Attack sequence
        self.game_control.attack()
        time.sleep(random.uniform(ATTACK_DELAY[0], ATTACK_DELAY[1]))

    def move_to_safe_spot(self):
        """Move character to safe spot"""
        if SAFE_SPOT_COORDINATES:
            self.logger.info("Moving to safe spot")
            self.game_control.move_to(
                SAFE_SPOT_COORDINATES[0],
                SAFE_SPOT_COORDINATES[1]
            )
            self.game_control.click()

    def stop(self):
        """Stop the bot"""
        self.logger.info("Stopping Tibia Bot...")
        self.running = False
        self.game_control.logout()

if __name__ == "__main__":
    bot = TibiaBot()
    bot.start() 