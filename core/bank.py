"""
Bank system for the Text RPG game.
"""
from typing import Dict, List, Optional, Tuple
from core.inventory import Item

class BankSlot:
    """Represents a single bank slot that can hold an item and quantity."""
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
        
        if self.item.name == item.name:
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

class Bank:
    """
    Bank system that stores items with a larger capacity than inventory.
    """
    def __init__(self, max_slots: int = 1000):
        """
        Initialize a new bank.
        
        Args:
            max_slots: Maximum number of bank slots
        """
        self.max_slots = max_slots
        self.slots = [BankSlot() for _ in range(max_slots)]
    
    def deposit(self, item: Item, quantity: int = 1) -> bool:
        """
        Deposit an item into the bank.
        
        Args:
            item: The item to deposit
            quantity: How many of the item to deposit
            
        Returns:
            bool: True if all items were deposited, False if some couldn't fit
        """
        remaining = quantity
        
        # First try to add to existing stacks
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name == item.name:
                remaining = slot.add_item(item, remaining)
                if remaining == 0:
                    return True
        
        # Then try to add to empty slots
        for slot in self.slots:
            if slot.is_empty():
                remaining = slot.add_item(item, remaining)
                if remaining == 0:
                    return True
        
        return False  # Couldn't deposit all items
    
    def withdraw(self, item_name: str, quantity: int = 1) -> Tuple[Optional[Item], int]:
        """
        Withdraw items from the bank.
        
        Args:
            item_name: Name of the item to withdraw
            quantity: How many to withdraw
            
        Returns:
            Tuple[Optional[Item], int]: The item and quantity withdrawn
        """
        remaining = quantity
        withdrawn_item = None
        total_withdrawn = 0
        
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name == item_name:
                item, qty_withdrawn = slot.remove_item(remaining)
                if withdrawn_item is None and item is not None:
                    withdrawn_item = item
                
                total_withdrawn += qty_withdrawn
                remaining -= qty_withdrawn
                
                if remaining == 0:
                    break
        
        return withdrawn_item, total_withdrawn
    
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Check if the bank has a specific item.
        
        Args:
            item_name: Name of the item to check
            quantity: Minimum quantity required
            
        Returns:
            bool: True if the bank has enough of the item
        """
        total = 0
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name == item_name:
                total += slot.quantity
                if total >= quantity:
                    return True
        return False
    
    def count_item(self, item_name: str) -> int:
        """
        Count how many of a specific item are in the bank.
        
        Args:
            item_name: Name of the item to count
            
        Returns:
            int: Total quantity of the item
        """
        total = 0
        for slot in self.slots:
            if not slot.is_empty() and slot.item.name == item_name:
                total += slot.quantity
        return total
    
    def count_items(self) -> int:
        """
        Count how many slots are used in the bank.
        
        Returns:
            int: Number of used slots
        """
        return sum(1 for slot in self.slots if not slot.is_empty())
    
    def is_full(self) -> bool:
        """
        Check if the bank is full.
        
        Returns:
            bool: True if all slots are used
        """
        return all(not slot.is_empty() for slot in self.slots)
    
    def display(self) -> str:
        """
        Get a string representation of the bank contents.
        
        Returns:
            str: Formatted bank display
        """
        result = [f"Bank ({self.count_items()}/{self.max_slots} slots):"]
        
        # Group items by category for better organization
        categories = {}
        
        for slot in self.slots:
            if not slot.is_empty():
                category = "Miscellaneous"
                item_name = slot.item.name.lower()
                
                if "ore" in item_name:
                    category = "Ores"
                elif any(tool in item_name for tool in ["pickaxe", "chisel", "ring", "cape"]):
                    category = "Equipment"
                elif "pet" in item_name or any(creature in item_name for creature in ["butterfly", "bat", "owl", "phoenix"]):
                    category = "Collectibles"
                
                if category not in categories:
                    categories[category] = []
                
                categories[category].append(f"  {slot.item.name} x{slot.quantity}")
        
        if not categories:
            result.append("  (Empty)")
        else:
            for category, items in sorted(categories.items()):
                result.append(f"\n{category}:")
                result.extend(sorted(items))
        
        return "\n".join(result)