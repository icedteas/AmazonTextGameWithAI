"""
Crafting skill implementation for the Text RPG game.
"""
import random
import time
from typing import Dict, List, Tuple, Optional
from core.inventory import Item
from core.equipment import EquipmentItem

class CraftableItem:
    """Represents an item that can be crafted."""
    def __init__(self, name: str, level_req: int, materials: Dict[str, int], 
                 xp: int, equipment_slot: Optional[str] = None, bonuses: Dict[str, float] = None):
        self.name = name
        self.level_req = level_req
        self.materials = materials  # Dict of material name -> quantity
        self.xp = xp
        self.equipment_slot = equipment_slot
        self.bonuses = bonuses or {}
    
    def __str__(self) -> str:
        return self.name
    
    def get_materials_str(self) -> str:
        """Get a string representation of required materials."""
        return ", ".join(f"{qty} {mat}" for mat, qty in self.materials.items())

class CraftingSkill:
    """
    Implementation of the crafting skill.
    """
    def __init__(self):
        """Initialize the crafting skill with craftable items."""
        self.craftable_items = self._initialize_craftable_items()
        self.easter_eggs = {
            "Crafting Pet": 0.00005,    # 1/20000 chance
            "Butterfly": 1/350,         # 1/350 chance
            "Bat": 1/500,               # 1/500 chance
            "Owl": 1/1000,              # 1/1000 chance
            "Phoenix": 1/20000          # 1/20000 chance
        }
    
    def _initialize_craftable_items(self) -> Dict[str, CraftableItem]:
        """
        Initialize all craftable items.
        
        Returns:
            Dict[str, CraftableItem]: Dictionary of item name to CraftableItem object
        """
        items = {}
        
        # Define tiers of materials and their properties
        tiers = [
            {"name": "Bronze", "level": 1, "material": "Bronze Ore", "qty": 2, "xp": 15, "bonus": 0.05},
            {"name": "Iron", "level": 5, "material": "Iron Ore", "qty": 3, "xp": 30, "bonus": 0.10},
            {"name": "Mithril", "level": 15, "material": "Mithril Ore", "qty": 4, "xp": 50, "bonus": 0.15},
            {"name": "Adamant", "level": 30, "material": "Adamant Ore", "qty": 5, "xp": 80, "bonus": 0.20},
            {"name": "Coal", "level": 50, "material": "Coal Ore", "qty": 6, "xp": 100, "bonus": 0.25},
            {"name": "Rune", "level": 65, "material": "Rune Ore", "qty": 7, "xp": 125, "bonus": 0.30},
            {"name": "Dragon", "level": 75, "material": "Dragon Ore", "qty": 8, "xp": 150, "bonus": 0.35},
            {"name": "Elite", "level": 85, "material": "Elite Ore", "qty": 9, "xp": 200, "bonus": 0.40},
            {"name": "King", "level": 95, "material": "King Ore", "qty": 10, "xp": 250, "bonus": 0.45}
        ]
        
        # Create items for each tier
        for tier in tiers:
            # Ring
            ring_name = f"{tier['name']} Ring"
            items[ring_name.lower()] = CraftableItem(
                ring_name,
                tier["level"],
                {tier["material"]: tier["qty"]},
                tier["xp"],
                "ring",
                {"mining_speed": tier["bonus"] * 0.5, "extra_ore_chance": tier["bonus"] * 0.3}
            )
            
            # Pickaxe (main hand)
            pickaxe_name = f"{tier['name']} Pickaxe"
            items[pickaxe_name.lower()] = CraftableItem(
                pickaxe_name,
                tier["level"],
                {tier["material"]: tier["qty"] * 2},
                tier["xp"] * 2,
                "main_hand",
                {"mining_speed": tier["bonus"], "extra_ore_chance": tier["bonus"] * 0.5}
            )
            
            # Chisel (off hand)
            chisel_name = f"{tier['name']} Chisel"
            items[chisel_name.lower()] = CraftableItem(
                chisel_name,
                tier["level"],
                {tier["material"]: tier["qty"]},
                tier["xp"],
                "off_hand",
                {"mining_speed": tier["bonus"] * 0.3, "extra_ore_chance": tier["bonus"]}
            )
            
            # Cape
            cape_colors = {
                "Bronze": "Brown", "Iron": "Gray", "Mithril": "Dark Blue",
                "Adamant": "Green", "Coal": "Black", "Rune": "Light Blue",
                "Dragon": "Red", "Elite": "Orange", "King": "Yellow"
            }
            cape_name = f"{cape_colors[tier['name']]} Cape"
            items[cape_name.lower()] = CraftableItem(
                cape_name,
                tier["level"],
                {tier["material"]: tier["qty"] * 3},
                tier["xp"] * 3,
                "cape",
                {"mining_speed": tier["bonus"] * 0.4, "extra_ore_chance": tier["bonus"] * 0.4}
            )
        
        return items
    
    def get_available_items(self, crafting_level: int) -> List[CraftableItem]:
        """
        Get items available to craft at the player's crafting level.
        
        Args:
            crafting_level: Player's current crafting level
            
        Returns:
            List[CraftableItem]: List of available craftable items
        """
        return [item for item in self.craftable_items.values() if item.level_req <= crafting_level]
    
    def craft_item(self, item_name: str, crafting_level: int, has_materials: bool, 
                   count: int = 1, material_count: int = 0) -> List[Tuple[Optional[Item], int, Optional[str]]]:
        """
        Craft an item if the player has the required level and materials.
        
        Args:
            item_name: Name of the item to craft
            crafting_level: Player's current crafting level
            has_materials: Whether the player has the required materials
            count: Number of items to craft (1-100)
            material_count: How many of the required materials the player has
            
        Returns:
            List[Tuple[Optional[Item], int, Optional[str]]]: 
                List of tuples containing:
                - The crafted item (or None if failed)
                - XP gained
                - Easter egg obtained (or None if none)
        """
        # Convert item_name to lowercase for case-insensitive lookup
        item_key = item_name.lower()
        
        if item_key not in self.craftable_items:
            print(f"Invalid item: {item_name}")
            return []
        
        craftable_item = self.craftable_items[item_key]
        
        if crafting_level < craftable_item.level_req:
            print(f"You need a Crafting level of {craftable_item.level_req} to craft {craftable_item.name}.")
            return []
        
        if not has_materials:
            print(f"You don't have the required materials: {craftable_item.get_materials_str()}")
            return []
        
        # Ensure count is within limits
        count = max(1, min(100, count))
        
        # If material_count is provided, limit count based on available materials
        if material_count > 0:
            # Calculate how many items can be crafted with available materials
            # This is simplified - in reality would need to check each material type
            max_craftable = material_count // list(craftable_item.materials.values())[0]
            count = min(count, max_craftable)
            
            if count == 0:
                print(f"You don't have enough materials to craft any {craftable_item.name}.")
                return []
        
        # For batch crafting, show progress
        if count > 1:
            print(f"Crafting {count} {craftable_item.name}...")
            
            # Show progress updates
            progress_interval = max(1, count // 10)
            craft_time = 1.0  # Base time for crafting one item
            
            for i in range(count):
                if i % progress_interval == 0 or i == count - 1:
                    progress = (i + 1) / count * 100
                    print(f"Progress: {progress:.1f}% ({i + 1}/{count})")
                time.sleep(craft_time * 0.5)  # Reduced time for batch crafting
        else:
            # Single crafting action
            print(f"Crafting a {craftable_item.name}...")
            time.sleep(1.5)  # Slightly longer for single item for better feedback
        
        results = []
        
        for _ in range(count):
            # Create the crafted item
            if craftable_item.equipment_slot:
                # Equipment item
                crafted_item = EquipmentItem(
                    craftable_item.name,
                    craftable_item.equipment_slot,
                    craftable_item.level_req,
                    f"A {craftable_item.name.lower()} crafted from ore"
                )
                crafted_item.bonuses = craftable_item.bonuses
            else:
                # Regular item
                crafted_item = Item(
                    craftable_item.name,
                    f"A {craftable_item.name.lower()} crafted from ore",
                    False
                )
            
            # Calculate XP
            xp_gained = craftable_item.xp
            
            # Check for easter eggs
            easter_egg = None
            for egg_name, chance in self.easter_eggs.items():
                if random.random() < chance:
                    easter_egg = egg_name
                    print(f"You found a {easter_egg} while crafting!")
                    break
            
            results.append((crafted_item, xp_gained, easter_egg))
        
        print(f"You crafted {count} {craftable_item.name}.")
        
        return results