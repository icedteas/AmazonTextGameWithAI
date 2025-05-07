"""
Collection log system for the Text RPG game.
"""
from typing import Dict, List, Set

class CollectionLog:
    """
    Collection log that tracks items obtained and achievements.
    """
    def __init__(self):
        """Initialize the collection log."""
        self.crafted_items = {}  # Item name -> count
        self.easter_eggs = {}    # Easter egg name -> count
        self.achievements = set()  # Set of achievement names
    
    def add_crafted_item(self, item_name: str, count: int = 1) -> None:
        """
        Record a crafted item in the collection log.
        
        Args:
            item_name: Name of the crafted item
            count: How many were crafted
        """
        if item_name in self.crafted_items:
            self.crafted_items[item_name] += count
        else:
            self.crafted_items[item_name] = count
            print(f"New collection log entry: {item_name}")
    
    def add_easter_egg(self, easter_egg_name: str) -> None:
        """
        Record an easter egg item in the collection log.
        
        Args:
            easter_egg_name: Name of the easter egg
        """
        if easter_egg_name in self.easter_eggs:
            self.easter_eggs[easter_egg_name] += 1
        else:
            self.easter_eggs[easter_egg_name] = 1
            print(f"New collection log entry: {easter_egg_name}")
    
    def add_achievement(self, achievement_name: str) -> None:
        """
        Record an achievement in the collection log.
        
        Args:
            achievement_name: Name of the achievement
        """
        if achievement_name not in self.achievements:
            self.achievements.add(achievement_name)
            print(f"New achievement: {achievement_name}")
    
    def has_crafted_item(self, item_name: str) -> bool:
        """
        Check if an item has been crafted.
        
        Args:
            item_name: Name of the item
            
        Returns:
            bool: True if the item has been crafted
        """
        return item_name in self.crafted_items
    
    def has_easter_egg(self, easter_egg_name: str) -> bool:
        """
        Check if an easter egg has been found.
        
        Args:
            easter_egg_name: Name of the easter egg
            
        Returns:
            bool: True if the easter egg has been found
        """
        return easter_egg_name in self.easter_eggs
    
    def has_achievement(self, achievement_name: str) -> bool:
        """
        Check if an achievement has been earned.
        
        Args:
            achievement_name: Name of the achievement
            
        Returns:
            bool: True if the achievement has been earned
        """
        return achievement_name in self.achievements
    
    def get_completion_percentage(self) -> float:
        """
        Calculate the overall completion percentage.
        
        Returns:
            float: Percentage of collection log completed
        """
        # Define the total number of possible items
        total_craftable_items = 27  # 9 tiers * 3 item types (ring, pickaxe, chisel)
        total_easter_eggs = 7       # Mining pet, Crafting pet, Magic pet, Butterfly, Bat, Owl, Phoenix
        
        # Count how many unique items have been collected
        crafted_count = len(self.crafted_items)
        easter_egg_count = len(self.easter_eggs)
        
        # Calculate percentage
        total_possible = total_craftable_items + total_easter_eggs
        total_collected = crafted_count + easter_egg_count
        
        return (total_collected / total_possible) * 100 if total_possible > 0 else 0
    
    def display(self) -> str:
        """
        Get a string representation of the collection log.
        
        Returns:
            str: Formatted collection log display
        """
        completion = self.get_completion_percentage()
        result = [f"Collection Log ({completion:.1f}% complete):"]
        
        # Crafted items section
        result.append("\nCrafted Items:")
        if not self.crafted_items:
            result.append("  None")
        else:
            # Group by tier
            tiers = {
                "Bronze": [],
                "Iron": [],
                "Mithril": [],
                "Adamant": [],
                "Coal": [],
                "Rune": [],
                "Dragon": [],
                "Elite": [],
                "King": []
            }
            
            for item_name, count in self.crafted_items.items():
                for tier in tiers:
                    if tier.lower() in item_name.lower():
                        tiers[tier].append(f"  {item_name} x{count}")
                        break
            
            for tier, items in tiers.items():
                if items:
                    result.append(f"  {tier}:")
                    result.extend(sorted(items))
        
        # Easter eggs section
        result.append("\nEaster Eggs:")
        if not self.easter_eggs:
            result.append("  None")
        else:
            # Group by type
            categories = {
                "Pets": [],
                "Creatures": []
            }
            
            for item_name, count in self.easter_eggs.items():
                if "Pet" in item_name:
                    categories["Pets"].append(f"  {item_name} x{count}")
                else:
                    categories["Creatures"].append(f"  {item_name} x{count}")
            
            for category, items in categories.items():
                if items:
                    result.append(f"  {category}:")
                    result.extend(sorted(items))
        
        # Achievements section
        result.append("\nAchievements:")
        if not self.achievements:
            result.append("  None")
        else:
            for achievement in sorted(self.achievements):
                result.append(f"  {achievement}")
        
        return "\n".join(result)