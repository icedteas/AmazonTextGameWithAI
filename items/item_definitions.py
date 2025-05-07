"""
Item definitions for the Text RPG game.
"""
from typing import Dict, List
from core.inventory import Item
from core.equipment import EquipmentItem

def create_ore_items() -> Dict[str, Item]:
    """
    Create all ore items.
    
    Returns:
        Dict[str, Item]: Dictionary of ore name to Item object
    """
    ores = {}
    
    # Define all ore types
    ore_types = [
        ("Bronze Ore", "A chunk of bronze ore"),
        ("Iron Ore", "A chunk of iron ore"),
        ("Mithril Ore", "A chunk of mithril ore"),
        ("Adamant Ore", "A chunk of adamant ore"),
        ("Coal Ore", "A chunk of coal ore"),
        ("Rune Ore", "A chunk of rune ore"),
        ("Dragon Ore", "A chunk of dragon ore"),
        ("Elite Ore", "A chunk of elite ore"),
        ("King Ore", "A chunk of king ore")
    ]
    
    # Create all ore items (all stackable)
    for name, description in ore_types:
        ores[name] = Item(name, description, True)
    
    return ores

def create_equipment_items() -> Dict[str, EquipmentItem]:
    """
    Create all equipment items.
    
    Returns:
        Dict[str, EquipmentItem]: Dictionary of equipment name to EquipmentItem object
    """
    equipment = {}
    
    # Define tiers with their properties
    tiers = [
        {"name": "Bronze", "level": 1, "bonus": 0.05},
        {"name": "Iron", "level": 5, "bonus": 0.10},
        {"name": "Mithril", "level": 15, "bonus": 0.15},
        {"name": "Adamant", "level": 30, "bonus": 0.20},
        {"name": "Coal", "level": 50, "bonus": 0.25},
        {"name": "Rune", "level": 65, "bonus": 0.30},
        {"name": "Dragon", "level": 75, "bonus": 0.35},
        {"name": "Elite", "level": 85, "bonus": 0.40},
        {"name": "King", "level": 95, "bonus": 0.45}
    ]
    
    # Create equipment for each tier
    for tier in tiers:
        # Ring
        ring_name = f"{tier['name']} Ring"
        ring = EquipmentItem(
            ring_name,
            "ring",
            tier["level"],
            f"A {tier['name'].lower()} ring that boosts mining abilities"
        )
        ring.bonuses = {
            "mining_speed": tier["bonus"] * 0.5,
            "extra_ore_chance": tier["bonus"] * 0.3
        }
        equipment[ring_name] = ring
        
        # Pickaxe (main hand)
        pickaxe_name = f"{tier['name']} Pickaxe"
        pickaxe = EquipmentItem(
            pickaxe_name,
            "main_hand",
            tier["level"],
            f"A {tier['name'].lower()} pickaxe for mining"
        )
        pickaxe.bonuses = {
            "mining_speed": tier["bonus"],
            "extra_ore_chance": tier["bonus"] * 0.5
        }
        equipment[pickaxe_name] = pickaxe
        
        # Chisel (off hand)
        chisel_name = f"{tier['name']} Chisel"
        chisel = EquipmentItem(
            chisel_name,
            "off_hand",
            tier["level"],
            f"A {tier['name'].lower()} chisel for precise mining"
        )
        chisel.bonuses = {
            "mining_speed": tier["bonus"] * 0.3,
            "extra_ore_chance": tier["bonus"]
        }
        equipment[chisel_name] = chisel
    
    # Create capes
    cape_colors = {
        "Bronze": "Brown", "Iron": "Gray", "Mithril": "Dark Blue",
        "Adamant": "Green", "Coal": "Black", "Rune": "Light Blue",
        "Dragon": "Red", "Elite": "Orange", "King": "Yellow"
    }
    
    for tier in tiers:
        cape_name = f"{cape_colors[tier['name']]} Cape"
        cape = EquipmentItem(
            cape_name,
            "cape",
            tier["level"],
            f"A {cape_colors[tier['name']].lower()} cape that enhances mining"
        )
        cape.bonuses = {
            "mining_speed": tier["bonus"] * 0.4,
            "extra_ore_chance": tier["bonus"] * 0.4
        }
        equipment[cape_name] = cape
    
    # Create skill capes
    for skill in ["Mining", "Crafting", "Magic"]:
        cape_name = f"{skill} Skill Cape"
        cape = EquipmentItem(
            cape_name,
            "cape",
            99,
            f"A cape showing mastery of the {skill} skill"
        )
        cape.bonuses = {
            "mining_speed": 0.5,
            "extra_ore_chance": 0.5
        }
        equipment[cape_name] = cape
    
    return equipment

def create_powerup_items() -> Dict[str, Item]:
    """
    Create all powerup items.
    
    Returns:
        Dict[str, Item]: Dictionary of powerup name to Item object
    """
    powerups = {}
    
    # Define powerups
    powerup_types = [
        ("Faster Mining Powerup", "Increases mining speed for a limited time"),
        ("Double XP Powerup", "Doubles all experience gained for a limited time"),
        ("5x Ore Chance Powerup", "Gives a chance to mine 5x ores at once")
    ]
    
    # Create all powerup items (all stackable)
    for name, description in powerup_types:
        powerups[name] = Item(name, description, True)
    
    return powerups

def create_easter_egg_items() -> Dict[str, Item]:
    """
    Create all easter egg items.
    
    Returns:
        Dict[str, Item]: Dictionary of easter egg name to Item object
    """
    easter_eggs = {}
    
    # Define easter eggs
    easter_egg_types = [
        ("Mining Pet", "A rare pet obtained while mining"),
        ("Crafting Pet", "A rare pet obtained while crafting"),
        ("Magic Pet", "A rare pet obtained while using magic"),
        ("Butterfly", "A rare butterfly you caught"),
        ("Bat", "A rare bat you befriended"),
        ("Owl", "A rare owl that decided to follow you"),
        ("Phoenix", "An extremely rare phoenix that chose you")
    ]
    
    # Create all easter egg items (not stackable)
    for name, description in easter_egg_types:
        easter_eggs[name] = Item(name, description, False)
    
    return easter_eggs

# Create all items
ORE_ITEMS = create_ore_items()
EQUIPMENT_ITEMS = create_equipment_items()
POWERUP_ITEMS = create_powerup_items()
EASTER_EGG_ITEMS = create_easter_egg_items()

# Combined dictionary of all items
ALL_ITEMS = {}
ALL_ITEMS.update(ORE_ITEMS)
ALL_ITEMS.update(EQUIPMENT_ITEMS)
ALL_ITEMS.update(POWERUP_ITEMS)
ALL_ITEMS.update(EASTER_EGG_ITEMS)