"""
Tibia Monsters Database
This file contains information about monsters in Tibia, organized by categories.
Data sourced from TibiaWiki.
"""

MONSTERS = {
    "Low Level (1-20)": {
        "Rats": {
            "Rat": {"level": 1, "hp": 20, "exp": 5, "loot": ["rat tail", "gold"]},
            "Cave Rat": {"level": 2, "hp": 25, "exp": 8, "loot": ["rat tail", "gold"]},
            "Giant Spider": {"level": 3, "hp": 40, "exp": 15, "loot": ["spider fangs", "gold"]},
            "Poison Spider": {"level": 4, "hp": 45, "exp": 20, "loot": ["spider fangs", "gold"]}
        },
        "Humans": {
            "Bandit": {"level": 5, "hp": 50, "exp": 25, "loot": ["gold", "knife", "rope"]},
            "Smuggler": {"level": 6, "hp": 55, "exp": 30, "loot": ["gold", "rope", "knife"]},
            "Pirate": {"level": 7, "hp": 60, "exp": 35, "loot": ["gold", "rope", "knife"]}
        },
        "Undead": {
            "Skeleton": {"level": 8, "hp": 65, "exp": 40, "loot": ["bone", "gold"]},
            "Ghost": {"level": 9, "hp": 70, "exp": 45, "loot": ["ghostly tissue", "gold"]},
            "Zombie": {"level": 10, "hp": 75, "exp": 50, "loot": ["rotten piece of cloth", "gold"]}
        }
    },
    "Medium Level (21-50)": {
        "Dragons": {
            "Dragon": {"level": 21, "hp": 1000, "exp": 200, "loot": ["dragon ham", "dragon scale", "gold"]},
            "Dragon Lord": {"level": 25, "hp": 1500, "exp": 300, "loot": ["dragon ham", "dragon scale", "gold"]},
            "Dragon Hatchling": {"level": 15, "hp": 500, "exp": 100, "loot": ["dragon ham", "gold"]}
        },
        "Demons": {
            "Demon": {"level": 30, "hp": 2000, "exp": 400, "loot": ["demon dust", "gold"]},
            "Demon Skeleton": {"level": 35, "hp": 2500, "exp": 500, "loot": ["demon dust", "gold"]},
            "Demon Outcast": {"level": 40, "hp": 3000, "exp": 600, "loot": ["demon dust", "gold"]}
        },
        "Giants": {
            "Cyclops": {"level": 25, "hp": 1500, "exp": 300, "loot": ["cyclops toe", "gold"]},
            "Cyclops Drone": {"level": 30, "hp": 2000, "exp": 400, "loot": ["cyclops toe", "gold"]},
            "Cyclops Smith": {"level": 35, "hp": 2500, "exp": 500, "loot": ["cyclops toe", "gold"]}
        }
    },
    "High Level (51+)": {
        "Bosses": {
            "Orshabaal": {"level": 100, "hp": 100000, "exp": 20000, "loot": ["gold", "rare items"]},
            "Ghazbaran": {"level": 90, "hp": 90000, "exp": 18000, "loot": ["gold", "rare items"]},
            "Ferumbras": {"level": 80, "hp": 80000, "exp": 16000, "loot": ["gold", "rare items"]}
        },
        "Elite Monsters": {
            "Dragon Lord": {"level": 60, "hp": 4000, "exp": 800, "loot": ["dragon ham", "dragon scale", "gold"]},
            "Demon": {"level": 70, "hp": 5000, "exp": 1000, "loot": ["demon dust", "gold"]},
            "Hydra": {"level": 80, "hp": 6000, "exp": 1200, "loot": ["hydra head", "gold"]}
        }
    }
}

# Monster categories for easy reference
MONSTER_CATEGORIES = {
    "Low Level": ["Rats", "Humans", "Undead"],
    "Medium Level": ["Dragons", "Demons", "Giants"],
    "High Level": ["Bosses", "Elite Monsters"]
}

# Common loot items and their values
LOOT_TABLE = {
    "gold": {"value": 1, "weight": 0.1},
    "dragon ham": {"value": 100, "weight": 1.0},
    "dragon scale": {"value": 200, "weight": 0.5},
    "demon dust": {"value": 150, "weight": 0.3},
    "cyclops toe": {"value": 80, "weight": 0.8},
    "hydra head": {"value": 300, "weight": 2.0},
    "spider fangs": {"value": 20, "weight": 0.2},
    "rat tail": {"value": 10, "weight": 0.1},
    "bone": {"value": 15, "weight": 0.3},
    "ghostly tissue": {"value": 25, "weight": 0.2}
}

def get_monster_info(monster_name):
    """Get information about a specific monster"""
    for category in MONSTERS.values():
        for subcategory in category.values():
            if monster_name in subcategory:
                return subcategory[monster_name]
    return None

def get_monsters_by_level_range(min_level, max_level):
    """Get all monsters within a specific level range"""
    monsters = []
    for category in MONSTERS.values():
        for subcategory in category.values():
            for monster_name, info in subcategory.items():
                if min_level <= info["level"] <= max_level:
                    monsters.append((monster_name, info))
    return monsters

def get_monsters_by_category(category):
    """Get all monsters in a specific category"""
    if category in MONSTERS:
        return MONSTERS[category]
    return None

def get_loot_value(item_name):
    """Get the value of a specific loot item"""
    return LOOT_TABLE.get(item_name, {"value": 0, "weight": 0}) 