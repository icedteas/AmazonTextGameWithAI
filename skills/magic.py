"""
Magic skill implementation for the Text RPG game.
"""
import random
import time
from typing import Dict, List, Tuple, Optional
from core.inventory import Item

class AlchemyItem:
    """Represents an item that can be alchemized for gold."""
    def __init__(self, name: str, gold_value: int, level_req: int):
        self.name = name
        self.gold_value = gold_value
        self.level_req = level_req
    
    def __str__(self) -> str:
        return f"{self.name} ({self.gold_value} gold)"

class MagicSkill:
    """
    Implementation of the magic skill.
    """
    def __init__(self):
        """Initialize the magic skill with alchemy values."""
        self.alchemy_values = self._initialize_alchemy_values()
        self.easter_eggs = {
            "Magic Pet": 0.00005,       # 1/20000 chance
            "Butterfly": 1/350,         # 1/350 chance
            "Bat": 1/500,               # 1/500 chance
            "Owl": 1/1000,              # 1/1000 chance
            "Phoenix": 1/20000          # 1/20000 chance
        }
    
    def _initialize_alchemy_values(self) -> Dict[str, AlchemyItem]:
        """
        Initialize alchemy values for different items.
        
        Returns:
            Dict[str, AlchemyItem]: Dictionary of item name to AlchemyItem object
        """
        alchemy_items = {}
        
        # Define tiers of items and their alchemy values
        tiers = [
            {"name": "Bronze", "value": 5, "level": 1},
            {"name": "Iron", "value": 10, "level": 5},
            {"name": "Mithril", "value": 20, "level": 15},
            {"name": "Adamant", "value": 45, "level": 30},
            {"name": "Coal", "value": 65, "level": 50},
            {"name": "Rune", "value": 85, "level": 65},
            {"name": "Dragon", "value": 100, "level": 75},
            {"name": "Elite", "value": 150, "level": 85},
            {"name": "King", "value": 250, "level": 95}
        ]
        
        # Create alchemy values for each tier and item type
        for tier in tiers:
            # Add equipment items
            for item_type in ["Ring", "Pickaxe", "Chisel"]:
                item_name = f"{tier['name']} {item_type}"
                alchemy_items[item_name.lower()] = AlchemyItem(
                    item_name,
                    tier["value"] * (2 if item_type == "Pickaxe" else 1),
                    tier["level"]
                )
            
            # Add capes
            cape_colors = {
                "Bronze": "Brown", "Iron": "Gray", "Mithril": "Dark Blue",
                "Adamant": "Green", "Coal": "Black", "Rune": "Light Blue",
                "Dragon": "Red", "Elite": "Orange", "King": "Yellow"
            }
            cape_name = f"{cape_colors[tier['name']]} Cape"
            alchemy_items[cape_name.lower()] = AlchemyItem(
                cape_name,
                tier["value"] * 3,
                tier["level"]
            )
        
        return alchemy_items
    
    def get_alchemy_value(self, item_name: str) -> int:
        """
        Get the alchemy value of an item.
        
        Args:
            item_name: Name of the item
            
        Returns:
            int: Gold value of the item, or 0 if not alchemizable
        """
        # Convert item_name to lowercase for case-insensitive lookup
        item_key = item_name.lower()
        
        if item_key in self.alchemy_values:
            return self.alchemy_values[item_key].gold_value
        return 0
    
    def can_alchemize(self, item_name: str, magic_level: int) -> bool:
        """
        Check if the player can alchemize an item.
        
        Args:
            item_name: Name of the item
            magic_level: Player's current magic level
            
        Returns:
            bool: True if the item can be alchemized at the player's level
        """
        # Convert item_name to lowercase for case-insensitive lookup
        item_key = item_name.lower()
        
        if item_key not in self.alchemy_values:
            return False
        
        return magic_level >= self.alchemy_values[item_key].level_req
    
    def alchemize(self, item_name: str, magic_level: int, count: int = 1) -> List[Tuple[int, int, Optional[str]]]:
        """
        Alchemize an item to get gold.
        
        Args:
            item_name: Name of the item to alchemize
            magic_level: Player's current magic level
            count: Number of items to alchemize (1-100)
            
        Returns:
            List[Tuple[int, int, Optional[str]]]: 
                List of tuples containing:
                - Gold obtained
                - XP gained
                - Easter egg obtained (or None if none)
        """
        # Convert item_name to lowercase for case-insensitive lookup
        item_key = item_name.lower()
        
        if item_key not in self.alchemy_values:
            print(f"Cannot alchemize {item_name}.")
            return []
        
        alchemy_item = self.alchemy_values[item_key]
        
        if magic_level < alchemy_item.level_req:
            print(f"You need a Magic level of {alchemy_item.level_req} to alchemize {item_name}.")
            return []
        
        # Ensure count is within limits
        count = max(1, min(100, count))
        
        # For batch alchemizing, show progress
        if count > 1:
            print(f"Alchemizing {count} {item_name}...")
            
            # Show progress updates
            progress_interval = max(1, count // 10)
            alch_time = 0.5  # Base time for alchemizing one item
            
            for i in range(count):
                if i % progress_interval == 0 or i == count - 1:
                    progress = (i + 1) / count * 100
                    print(f"Progress: {progress:.1f}% ({i + 1}/{count})")
                time.sleep(alch_time * 0.3)  # Reduced time for batch alchemizing
        else:
            # Single alchemizing action
            print(f"Alchemizing {item_name}...")
            time.sleep(0.8)  # Slightly longer for single item for better feedback
        
        results = []
        total_gold = 0
        
        for _ in range(count):
            # Calculate gold and XP
            gold = alchemy_item.gold_value
            xp = gold  # XP is equal to gold value
            
            # Check for easter eggs
            easter_egg = None
            for egg_name, chance in self.easter_eggs.items():
                if random.random() < chance:
                    easter_egg = egg_name
                    print(f"You found a {easter_egg} while alchemizing!")
                    break
            
            results.append((gold, xp, easter_egg))
            total_gold += gold
        
        print(f"You alchemized {count} {item_name} for a total of {total_gold} gold.")
        
        return results
    
    def get_available_alchemy_items(self, magic_level: int) -> List[AlchemyItem]:
        """
        Get items available to alchemize at the player's magic level.
        
        Args:
            magic_level: Player's current magic level
            
        Returns:
            List[AlchemyItem]: List of available alchemy items
        """
        return [item for item in self.alchemy_values.values() if item.level_req <= magic_level]