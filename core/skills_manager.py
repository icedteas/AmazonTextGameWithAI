"""
Skills management system for the Text RPG game.
"""
from typing import Dict, List
import math

class Skill:
    """Represents a single skill with experience and level tracking."""
    def __init__(self, name: str):
        self.name = name
        self.experience = 0
        self.max_level = 99
    
    def add_experience(self, amount: int) -> bool:
        """
        Add experience to the skill and check for level ups.
        
        Args:
            amount: Amount of experience to add
            
        Returns:
            bool: True if leveled up, False otherwise
        """
        old_level = self.get_level()
        self.experience += amount
        new_level = self.get_level()
        
        return new_level > old_level
    
    def get_level(self) -> int:
        """
        Calculate the current level based on experience.
        
        Returns:
            int: Current skill level (1-99)
        """
        # Exponential scaling formula for levels
        # Each level requires more XP than the previous
        if self.experience <= 0:
            return 1
        
        # This formula makes each level progressively harder to achieve
        level = int(1 + math.sqrt(self.experience / 100))
        return min(level, self.max_level)
    
    def get_experience_for_level(self, level: int) -> int:
        """
        Calculate the experience required for a specific level.
        
        Args:
            level: Target level
            
        Returns:
            int: Experience required
        """
        if level <= 1:
            return 0
        
        # Reverse of the level calculation formula
        return (level - 1) ** 2 * 100
    
    def get_progress_to_next_level(self) -> float:
        """
        Calculate progress percentage to the next level.
        
        Returns:
            float: Percentage progress (0-100)
        """
        current_level = self.get_level()
        
        if current_level >= self.max_level:
            return 100.0
        
        current_level_xp = self.get_experience_for_level(current_level)
        next_level_xp = self.get_experience_for_level(current_level + 1)
        xp_needed = next_level_xp - current_level_xp
        xp_gained = self.experience - current_level_xp
        
        return min(100.0, (xp_gained / xp_needed) * 100)

class SkillsManager:
    """
    Manages all player skills and their progression.
    """
    def __init__(self):
        """Initialize all skills at level 0."""
        self.skills = {
            "mining": Skill("Mining"),
            "crafting": Skill("Crafting"),
            "magic": Skill("Magic")
        }
    
    def add_experience(self, skill_name: str, amount: int, multiplier: float = 1.0) -> bool:
        """
        Add experience to a skill.
        
        Args:
            skill_name: Name of the skill
            amount: Base amount of experience to add
            multiplier: Experience multiplier (e.g., from powerups)
            
        Returns:
            bool: True if leveled up, False otherwise
        """
        if skill_name not in self.skills:
            print(f"Invalid skill: {skill_name}")
            return False
        
        adjusted_amount = int(amount * multiplier)
        leveled_up = self.skills[skill_name].add_experience(adjusted_amount)
        
        if leveled_up:
            new_level = self.get_level(skill_name)
            print(f"Congratulations! Your {skill_name.title()} level is now {new_level}!")
            
            # Check for unlocks at this level
            self._check_unlocks(skill_name, new_level)
        
        return leveled_up
    
    def get_level(self, skill_name: str) -> int:
        """
        Get the current level of a skill.
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            int: Current skill level
        """
        if skill_name not in self.skills:
            print(f"Invalid skill: {skill_name}")
            return 0
        
        return self.skills[skill_name].get_level()
    
    def get_experience(self, skill_name: str) -> int:
        """
        Get the current experience of a skill.
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            int: Current skill experience
        """
        if skill_name not in self.skills:
            print(f"Invalid skill: {skill_name}")
            return 0
        
        return self.skills[skill_name].experience
    
    def _check_unlocks(self, skill_name: str, level: int) -> None:
        """
        Check and announce any unlocks at the current level.
        
        Args:
            skill_name: Name of the skill
            level: Current level to check for unlocks
        """
        unlocks = {
            "mining": {
                1: "Bronze rocks",
                5: "Iron rocks",
                15: "Mithril rocks",
                30: "Adamant rocks",
                50: "Coal rocks",
                65: "Rune rocks",
                75: "Dragon rocks",
                85: "Elite rocks",
                95: "King rocks"
            },
            "crafting": {
                1: "Bronze equipment",
                5: "Iron equipment",
                15: "Mithril equipment",
                30: "Adamant equipment",
                50: "Coal equipment",
                65: "Rune equipment",
                75: "Dragon equipment",
                85: "Elite equipment",
                95: "King equipment"
            },
            "magic": {
                1: "Bronze alchemy",
                5: "Iron alchemy",
                15: "Mithril alchemy",
                30: "Adamant alchemy",
                50: "Coal alchemy",
                65: "Rune alchemy",
                75: "Dragon alchemy",
                85: "Elite alchemy",
                95: "King alchemy"
            }
        }
        
        if skill_name in unlocks and level in unlocks[skill_name]:
            print(f"Unlocked: {unlocks[skill_name][level]}!")
    
    def display_skill(self, skill_name: str) -> str:
        """
        Get a string representation of a skill's status.
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            str: Formatted skill display
        """
        if skill_name not in self.skills:
            return f"Invalid skill: {skill_name}"
        
        skill = self.skills[skill_name]
        level = skill.get_level()
        xp = skill.experience
        progress = skill.get_progress_to_next_level()
        
        if level >= skill.max_level:
            return f"{skill_name.title()}: Level {level} (max) - XP: {xp}"
        
        next_level_xp = skill.get_experience_for_level(level + 1)
        
        return f"{skill_name.title()}: Level {level} - XP: {xp}/{next_level_xp} ({progress:.1f}%)"
    
    def display_all_skills(self) -> str:
        """
        Get a string representation of all skills.
        
        Returns:
            str: Formatted skills display
        """
        result = ["Skills:"]
        
        for skill_name in sorted(self.skills.keys()):
            result.append("  " + self.display_skill(skill_name))
        
        return "\n".join(result)