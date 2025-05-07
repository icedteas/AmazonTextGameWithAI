"""
Shop system for the Text RPG game.
"""
from typing import Dict, List, Optional
from core.inventory import Item

class ShopItem:
    """Represents an item that can be purchased from the shop."""
    def __init__(self, name: str, description: str, price: int, item: Item):
        self.name = name
        self.description = description
        self.price = price
        self.item = item
    
    def __str__(self) -> str:
        return f"{self.name} - {self.price} gold"

class Shop:
    """
    Shop system that sells items to the player.
    """
    def __init__(self):
        """Initialize the shop with available items."""
        self.items = {}
        self._initialize_shop_items()
    
    def _initialize_shop_items(self) -> None:
        """Set up the initial shop inventory."""
        # Powerups
        self.add_item(
            ShopItem(
                "Faster Mining Rate",
                "Increases mining speed for a limited time",
                1000,
                Item("Faster Mining Powerup", "Increases mining speed", True)
            )
        )
        
        self.add_item(
            ShopItem(
                "Double Experience",
                "Doubles all experience gained for a limited time",
                5000,
                Item("Double XP Powerup", "Doubles all experience gained", True)
            )
        )
        
        self.add_item(
            ShopItem(
                "5x Ore Chance",
                "Gives a chance to mine 5x ores at once",
                5000,
                Item("5x Ore Chance Powerup", "Chance to mine 5x ores", True)
            )
        )
        
        # Skill capes
        self.add_item(
            ShopItem(
                "Mining Skill Cape",
                "A cape showing mastery of the Mining skill",
                750000,
                Item("Mining Skill Cape", "A symbol of Mining mastery", False)
            )
        )
        
        self.add_item(
            ShopItem(
                "Crafting Skill Cape",
                "A cape showing mastery of the Crafting skill",
                750000,
                Item("Crafting Skill Cape", "A symbol of Crafting mastery", False)
            )
        )
        
        self.add_item(
            ShopItem(
                "Magic Skill Cape",
                "A cape showing mastery of the Magic skill",
                750000,
                Item("Magic Skill Cape", "A symbol of Magic mastery", False)
            )
        )
    
    def add_item(self, shop_item: ShopItem) -> None:
        """
        Add an item to the shop.
        
        Args:
            shop_item: The shop item to add
        """
        self.items[shop_item.name] = shop_item
    
    def get_item(self, item_name: str) -> Optional[ShopItem]:
        """
        Get a shop item by name.
        
        Args:
            item_name: Name of the item to get
            
        Returns:
            Optional[ShopItem]: The shop item, if found
        """
        return self.items.get(item_name)
    
    def display(self) -> str:
        """
        Get a string representation of the shop.
        
        Returns:
            str: Formatted shop display
        """
        result = ["Shop Items:"]
        
        # Group items by category
        categories = {
            "Powerups": [],
            "Skill Capes": []
        }
        
        for item_name, shop_item in self.items.items():
            if "Cape" in item_name:
                categories["Skill Capes"].append(shop_item)
            else:
                categories["Powerups"].append(shop_item)
        
        for category, items in categories.items():
            if items:
                result.append(f"\n{category}:")
                for item in sorted(items, key=lambda x: x.price):
                    result.append(f"  {item.name} - {item.price} gold")
                    result.append(f"    {item.description}")
        
        return "\n".join(result)