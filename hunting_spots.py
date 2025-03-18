"""
Tibia Hunting Spots Database
This file contains information about hunting spots and their associated monsters.
"""

from monsters import MONSTERS, get_monster_info

HUNTING_SPOTS = {
    "Low Level Spots": {
        "Rookgaard": {
            "location": "Rookgaard",
            "level_range": (1, 8),
            "monsters": ["Rat", "Cave Rat", "Spider", "Poison Spider"],
            "requirements": None,
            "recommended_level": 1,
            "safety_level": "Very Safe",
            "loot_value": "Low"
        },
        "Dawnport": {
            "location": "Dawnport",
            "level_range": (1, 15),
            "monsters": ["Rat", "Cave Rat", "Spider", "Poison Spider", "Rotworm"],
            "requirements": None,
            "recommended_level": 1,
            "safety_level": "Very Safe",
            "loot_value": "Low"
        }
    },
    "Medium Level Spots": {
        "Dragon Lair": {
            "location": "Venore Dragon Lair",
            "level_range": (20, 40),
            "monsters": ["Dragon", "Dragon Hatchling", "Dragon Lord"],
            "requirements": "Fire Protection",
            "recommended_level": 25,
            "safety_level": "Medium",
            "loot_value": "High"
        },
        "Cyclopolis": {
            "location": "Edron Cyclopolis",
            "level_range": (25, 45),
            "monsters": ["Cyclops", "Cyclops Drone", "Cyclops Smith"],
            "requirements": "Physical Protection",
            "recommended_level": 30,
            "safety_level": "Medium",
            "loot_value": "Medium"
        }
    },
    "High Level Spots": {
        "Demon Lair": {
            "location": "Goroma",
            "level_range": (50, 100),
            "monsters": ["Demon", "Demon Skeleton", "Demon Outcast"],
            "requirements": "Fire Protection, Physical Protection",
            "recommended_level": 60,
            "safety_level": "Dangerous",
            "loot_value": "Very High"
        },
        "Hydra Island": {
            "location": "Oramond",
            "level_range": (70, 120),
            "monsters": ["Hydra", "Dragon Lord", "Demon"],
            "requirements": "Fire Protection, Physical Protection",
            "recommended_level": 80,
            "safety_level": "Very Dangerous",
            "loot_value": "Very High"
        }
    }
}

def get_hunting_spot_info(spot_name):
    """Get information about a specific hunting spot"""
    for category in HUNTING_SPOTS.values():
        if spot_name in category:
            return category[spot_name]
    return None

def get_spots_by_level_range(min_level, max_level):
    """Get all hunting spots suitable for a specific level range"""
    suitable_spots = []
    for category in HUNTING_SPOTS.values():
        for spot_name, info in category.items():
            if min_level >= info["recommended_level"]:
                suitable_spots.append((spot_name, info))
    return suitable_spots

def get_spots_by_safety_level(safety_level):
    """Get all hunting spots with a specific safety level"""
    spots = []
    for category in HUNTING_SPOTS.values():
        for spot_name, info in category.items():
            if info["safety_level"] == safety_level:
                spots.append((spot_name, info))
    return spots

def get_spots_by_loot_value(loot_value):
    """Get all hunting spots with a specific loot value"""
    spots = []
    for category in HUNTING_SPOTS.values():
        for spot_name, info in category.items():
            if info["loot_value"] == loot_value:
                spots.append((spot_name, info))
    return spots

def get_spot_monsters(spot_name):
    """Get detailed information about monsters in a specific hunting spot"""
    spot_info = get_hunting_spot_info(spot_name)
    if not spot_info:
        return None
    
    monsters = []
    for monster_name in spot_info["monsters"]:
        monster_info = get_monster_info(monster_name)
        if monster_info:
            monsters.append((monster_name, monster_info))
    
    return monsters 