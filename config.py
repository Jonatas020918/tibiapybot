import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Game Window Settings
GAME_WINDOW_TITLE = "Tibia"
SCREENSHOT_REGION = None  # Will be set dynamically based on game window

# Character Settings
MIN_HP_PERCENT = 70  # Minimum HP percentage before healing
MIN_MP_PERCENT = 30  # Minimum MP percentage before mana potion
EMERGENCY_HP_PERCENT = 40  # HP percentage to trigger emergency healing

# Hunting Settings
HUNTING_SPOTS = [
    {
        "name": "Default Spot",
        "coordinates": (0, 0),  # Will be set based on game window
        "monsters": ["monster1", "monster2"],
        "loot_items": ["gold", "item1", "item2"]
    }
]

# Loot Settings
LOOT_PRIORITY = {
    "gold": 1,
    "item1": 2,
    "item2": 3
}

# Safety Settings
PLAYER_DETECTION_ENABLED = True
LOGOUT_HP_PERCENT = 20
MAX_STUCK_TIME = 30  # seconds
SAFE_SPOT_COORDINATES = None  # Will be set based on game window

# Movement Settings
MOVEMENT_DELAY = (0.5, 2.0)  # Random delay between movements
ATTACK_DELAY = (1.0, 3.0)  # Random delay between attacks

# Screen Recognition Settings
TEMPLATE_MATCHING_THRESHOLD = 0.8
OCR_CONFIDENCE_THRESHOLD = 0.7

# Hotkeys
HOTKEYS = {
    "heal": "f1",
    "mana_potion": "f2",
    "attack": "f3",
    "loot": "f4",
    "logout": "f5"
}

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FILE = "tibia_bot.log"

# Anti-Detection Settings
RANDOM_MOVEMENTS = True
RANDOM_DELAYS = True
HUMAN_LIKE_MOVEMENT = True 