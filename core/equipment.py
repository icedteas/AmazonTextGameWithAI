"""
Equipment system for the Text RPG game.
"""
from typing import Dict, Optional, List

class EquipmentItem:
    """Base class for equipment items."""
    def __init__(self, name: str, slot: str, level_req: int, description: str):
        self.name = name
        self.slot = slot  # ring, main_hand, off_hand, cape
        self.level_req = level_req
        self.description = description
        self.bonuses = {}  # Mining speed, extra ore chance, etc.
        self.stackable = False  # Equipment items are never stackable
    
    def __str__(self) -> str:
        return f"{self.name} ({self.slot})"

class Equipment:
    """
    Equipment system that manages equipped items in different slots.
    """
    def __init__(self):
        """Initialize equipment slots."""
        self.slots = {
            "ring": None,
            "main_hand": None,  # Tool
            "off_hand": None,   # Off-hand tool
            "cape": None
        }
    
    def equip(self, item: EquipmentItem) -> Optional[EquipmentItem]:
        """
        Equip an item to its slot.
        
        Args:
            item: The item to equip
            
        Returns:
            Optional[EquipmentItem]: The previously equipped item, if any
        """
        if item.slot not in self.slots:
            print(f"Cannot equip {item.name}: invalid slot {item.slot}")
            return None
        
        old_item = self.slots[item.slot]
        self.slots[item.slot] = item
        return old_item
    
    def unequip(self, slot: str) -> Optional[EquipmentItem]:
        """
        Unequip an item from a slot.
        
        Args:
            slot: The equipment slot to unequip from
            
        Returns:
            Optional[EquipmentItem]: The unequipped item, if any
        """
        if slot not in self.slots:
            print(f"Invalid equipment slot: {slot}")
            return None
        
        item = self.slots[slot]
        self.slots[slot] = None
        return item
    
    def get_equipped(self, slot: str) -> Optional[EquipmentItem]:
        """
        Get the item equipped in a slot.
        
        Args:
            slot: The equipment slot to check
            
        Returns:
            Optional[EquipmentItem]: The equipped item, if any
        """
        if slot not in self.slots:
            print(f"Invalid equipment slot: {slot}")
            return None
        
        return self.slots[slot]
    
    def get_all_bonuses(self) -> Dict[str, float]:
        """
        Calculate total bonuses from all equipped items.
        
        Returns:
            Dict[str, float]: Combined bonuses from all equipment
        """
        total_bonuses = {}
        
        for slot, item in self.slots.items():
            if item is not None:
                for bonus_type, value in item.bonuses.items():
                    if bonus_type in total_bonuses:
                        total_bonuses[bonus_type] += value
                    else:
                        total_bonuses[bonus_type] = value
        
        return total_bonuses
    
    def display(self) -> str:
        """
        Get a string representation of equipped items.
        
        Returns:
            str: Formatted equipment display
        """
        result = ["Equipment:"]
        
        for slot, item in self.slots.items():
            slot_name = slot.replace('_', ' ').title()
            if item is None:
                result.append(f"  {slot_name}: None")
            else:
                result.append(f"  {slot_name}: {item.name}")
        
        return "\n".join(result)