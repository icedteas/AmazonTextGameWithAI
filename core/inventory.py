"""
Inventory system for the Text RPG game.
"""
from typing import Dict, List, Optional, Tuple

class Item:
    """Base class for all items in the game."""
    def __init__(self, name: str, description: str, stackable: bool = False):
        self.name = name
        self.description = description
        self.stackable = stackable
    
    def __str__(self) -> str:
        return self.name

class InventorySlot:
    """Represents a single inventory slot that can hold an item and quantity."""
    def __init__(self):
        self.item = None
        self.quantity = 0
    
    def is_empty(self) -> bool:
        """Check if the slot is empty."""
        return self.item is None
    
    def add_item(self, item: Item, quantity: int = 1) -> int:
        """
        Add an item to this slot.
        
        Args:
            item: The item to add
            quantity: How many of the item to add
            
        Returns:
            int: Overflow quantity that couldn't be added
        """
        if self.is_empty():
            self.item = item
            self.quantity = quantity
            return 0
        
        if self.item.name == item.name and self.item.stackable:
            self.quantity += quantity
            return 0
        
        return quantity  # Can't add to this slot
    
    def remove_item(self, quantity: int = 1) -> Tuple[Optional[Item], int]:
        """
        Remove items from this slot.
        
        Args:
            quantity: How many to remove
            
        Returns:
            Tuple[Optional[Item], int]: The item and quantity removed
        """
        if self.is_empty():
            return None, 0
        
        if quantity >= self.quantity:
            item = self.item
            removed = self.quantity
            self.item = None
            self.quantity = 0
            return item, removed
        
        self.quantity -= quantity
        return self.item, quantity

class Inventory:
    """
    Inventory system that manages a collection of items.
    """
    def __init__(self, max_slots: int):
        """
        Initialize a new inventory.
        
        Args:
            max_slots: Maximum number of inventory slots
        """
        self.max_slots = max_slots
        self.slots = [InventorySlot() for _ in range(max_slots)]
    
    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """
        Add an item to the inventory.
        
        Args:
            item: The item to add
            quantity: How many of the item to add
            
        Returns:
            bool: True if all items were added, False if some couldn't fit
        """
        remaining = quantity
        
        # First try to add to existing stacks if item is stackable
        if item.stackable:
            for slot in self.slots:
                if not slot.is_empty() and slot.item.name.lower() == item.name.lower():
                    remaining = slot.add_item(item, remaining)
                    if remaining == 0:
                        return True
        
        # Then try to add to empty slots
        for slot in self.slots:
            if slot.is_empty():
                remaining = slot.add_item(item, remaining)
                if remaining == 0:
                    return True
        
        return False  # Couldn't add all items
    
    def remove_item(self, item_name: str, quantity: int = 1) -> int:
        """
        Remove items from the inventory.
        
        Args:
            item_name: Name of the item to remove
            quantity: How many to remove
            
        Returns:
            int: How many were actually removed
        """
        item_name_lower = item_name.lower()
        remaining = quantity
        removed = 0
        
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name.lower() == item_name_lower:
                _, qty_removed = slot.remove_item(remaining)
                removed += qty_removed
                remaining -= qty_removed
                if remaining == 0:
                    break
        
        return removed
    
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Check if the inventory has a specific item.
        
        Args:
            item_name: Name of the item to check
            quantity: Minimum quantity required
            
        Returns:
            bool: True if the inventory has enough of the item
        """
        item_name_lower = item_name.lower()
        total = 0
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name.lower() == item_name_lower:
                total += slot.quantity
                if total >= quantity:
                    return True
        return False
    
    def count_item(self, item_name: str) -> int:
        """
        Count how many of a specific item are in the inventory.
        
        Args:
            item_name: Name of the item to count
            
        Returns:
            int: Total quantity of the item
        """
        item_name_lower = item_name.lower()
        total = 0
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name.lower() == item_name_lower:
                total += slot.quantity
        return total
    
    def count_items(self) -> int:
        """
        Count how many slots are used in the inventory.
        
        Returns:
            int: Number of used slots
        """
        return sum(1 for slot in self.slots if not slot.is_empty())
    
    def is_full(self) -> bool:
        """
        Check if the inventory is full.
        
        Returns:
            bool: True if all slots are used
        """
        return all(not slot.is_empty() for slot in self.slots)
    
    def display(self) -> str:
        """
        Get a string representation of the inventory.
        
        Returns:
            str: Formatted inventory display
        """
        result = [f"Inventory ({self.count_items()}/{self.max_slots} slots):"]
        
        for i, slot in enumerate(self.slots):
            if not slot.is_empty():
                result.append(f"{i+1}. {slot.item.name} x{slot.quantity}")
        
        if self.count_items() == 0:
            result.append("  (Empty)")
            
        return "\n".join(result)