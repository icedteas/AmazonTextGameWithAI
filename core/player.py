"""
Player class for the Text RPG game.
"""
from typing import Dict, List, Optional
from core.inventory import Inventory
from core.equipment import Equipment
from core.skills_manager import SkillsManager

class Player:
    """
    Player class that manages player attributes, inventory, equipment, and skills.
    """
    def __init__(self, name: str):
        """
        Initialize a new player.
        
        Args:
            name: The player's name
        """
        self.name = name
        self.gold = 0
        self.inventory = Inventory(28)  # 28 inventory slots
        self.equipment = Equipment()
        self.skills = SkillsManager()
        self.active_powerups = {
            "faster_mining": 0,
            "double_xp": 0,
            "chance_5x_ore": 0
        }
    
    def toggle_skills_interface(self) -> str:
        """Display all skills and their current XP levels."""
        return self.skills.display_all_skills()
    
    def add_gold(self, amount: int) -> None:
        """
        Add gold to the player's balance.
        
        Args:
            amount: Amount of gold to add
        """
        self.gold += amount
        print(f"+ {amount} gold. Total: {self.gold} gold")
    
    def spend_gold(self, amount: int) -> bool:
        """
        Spend gold if the player has enough.
        
        Args:
            amount: Amount of gold to spend
            
        Returns:
            bool: True if successful, False if not enough gold
        """
        if self.gold >= amount:
            self.gold -= amount
            print(f"- {amount} gold. Remaining: {self.gold} gold")
            return True
        else:
            print(f"Not enough gold. You have {self.gold}, need {amount}.")
            return False
    
    def activate_powerup(self, powerup_name: str) -> bool:
        """
        Activate a powerup if the player has it.
        
        Args:
            powerup_name: Name of the powerup to activate
            
        Returns:
            bool: True if successful, False if no powerup available
        """
        if powerup_name in self.active_powerups and self.active_powerups[powerup_name] > 0:
            self.active_powerups[powerup_name] += 1
            return True
        return False
    
    def has_active_powerup(self, powerup_name: str) -> bool:
        """
        Check if a powerup is active.
        
        Args:
            powerup_name: Name of the powerup to check
            
        Returns:
            bool: True if active, False otherwise
        """
        return self.active_powerups.get(powerup_name, 0) > 0
    
    def get_status(self) -> str:
        """
        Get a summary of the player's status.
        
        Returns:
            str: Player status summary
        """
        status = [
            f"Name: {self.name}",
            f"Gold: {self.gold}",
            f"Mining Level: {self.skills.get_level('mining')}",
            f"Crafting Level: {self.skills.get_level('crafting')}",
            f"Magic Level: {self.skills.get_level('magic')}",
            f"Inventory: {self.inventory.count_items()}/{self.inventory.max_slots} slots used"
        ]
        
        # Add active powerups
        active = [name for name, count in self.active_powerups.items() if count > 0]
        if active:
            status.append(f"Active Powerups: {', '.join(active)}")
        
        return "\n".join(status)