"""
Mining skill implementation for the Text RPG game.
"""
import random
import time
from typing import Dict, List, Tuple, Optional
from core.inventory import Item

class Rock:
    """Represents a rock that can be mined for ore."""
    def __init__(self, name: str, level_req: int, ore_name: str, base_time: float, base_xp: int):
        self.name = name
        self.level_req = level_req
        self.ore_name = ore_name
        self.base_time = base_time  # Base time in seconds to mine
        self.base_xp = base_xp      # Base XP for mining
    
    def __str__(self) -> str:
        return self.name

class MiningSkill:
    """
    Implementation of the mining skill.
    """
    def __init__(self):
        """Initialize the mining skill with available rocks."""
        self.rocks = self._initialize_rocks()
        self.easter_eggs = {
            "Mining Pet": 0.00005,      # 1/20000 chance
            "Butterfly": 1/350,         # 1/350 chance
            "Bat": 1/500,               # 1/500 chance
            "Owl": 1/1000,              # 1/1000 chance
            "Phoenix": 1/20000          # 1/20000 chance
        }
    
    def _initialize_rocks(self) -> Dict[str, Rock]:
        """
        Initialize all available rocks.
        
        Returns:
            Dict[str, Rock]: Dictionary of rock name to Rock object
        """
        return {
            "bronze": Rock("Bronze Rock", 1, "Bronze Ore", 3.0, 10),
            "iron": Rock("Iron Rock", 5, "Iron Ore", 5.0, 25),
            "mithril": Rock("Mithril Rock", 15, "Mithril Ore", 8.0, 50),
            "adamant": Rock("Adamant Rock", 30, "Adamant Ore", 12.0, 80),
            "coal": Rock("Coal Rock", 50, "Coal Ore", 15.0, 100),
            "rune": Rock("Rune Rock", 65, "Rune Ore", 20.0, 125),
            "dragon": Rock("Dragon Rock", 75, "Dragon Ore", 25.0, 150),
            "elite": Rock("Elite Rock", 85, "Elite Ore", 30.0, 200),
            "king": Rock("King Rock", 95, "King Ore", 35.0, 250)
        }
    
    def get_available_rocks(self, mining_level: int) -> List[Rock]:
        """
        Get rocks available at the player's mining level.
        
        Args:
            mining_level: Player's current mining level
            
        Returns:
            List[Rock]: List of available rocks
        """
        return [rock for rock in self.rocks.values() if rock.level_req <= mining_level]
    
    def mine_rock(self, rock_name: str, mining_level: int, equipment_bonuses: Dict[str, float] = None, 
                  has_faster_mining: bool = False, has_5x_ore_chance: bool = False, 
                  count: int = 1) -> List[Tuple[Optional[Item], int, Optional[str]]]:
        """
        Mine a rock to get ore.
        
        Args:
            rock_name: Name of the rock to mine
            mining_level: Player's current mining level
            equipment_bonuses: Bonuses from equipped items
            has_faster_mining: Whether the player has the faster mining powerup
            has_5x_ore_chance: Whether the player has the 5x ore chance powerup
            count: Number of mining attempts to perform (1-100)
            
        Returns:
            List[Tuple[Optional[Item], int, Optional[str]]]: 
                List of tuples containing:
                - The ore item obtained (or None if failed)
                - XP gained
                - Easter egg obtained (or None if none)
        """
        if rock_name not in self.rocks:
            print(f"Invalid rock: {rock_name}")
            return []
        
        rock = self.rocks[rock_name]
        
        if mining_level < rock.level_req:
            print(f"You need a Mining level of {rock.level_req} to mine {rock.name}.")
            return []
        
        # Ensure count is within limits
        count = max(1, min(100, count))
        
        # Calculate mining time based on level and equipment
        time_modifier = 1.0
        
        # Level bonus (higher level = faster mining)
        level_bonus = min(0.5, (mining_level - rock.level_req) / 100)
        time_modifier -= level_bonus
        
        # Equipment bonus
        if equipment_bonuses:
            mining_speed_bonus = equipment_bonuses.get("mining_speed", 0)
            time_modifier -= mining_speed_bonus
        
        # Powerup bonus
        if has_faster_mining:
            time_modifier -= 0.2
        
        # Ensure mining still takes some time
        time_modifier = max(0.3, time_modifier)
        
        # Calculate actual mining time
        mining_time = rock.base_time * time_modifier
        
        # For batch mining, reduce the time per action but still show progress
        if count > 1:
            # Reduce time for batch mining (more efficient)
            batch_time_reduction = 0.7  # 30% faster when batch mining
            total_mining_time = mining_time * count * batch_time_reduction
            
            print(f"Mining {count} {rock.name}...")
            
            # Show progress updates
            progress_interval = max(1, count // 10)
            for i in range(count):
                if i % progress_interval == 0 or i == count - 1:
                    progress = (i + 1) / count * 100
                    print(f"Progress: {progress:.1f}% ({i + 1}/{count})")
                time.sleep(mining_time * batch_time_reduction)
        else:
            # Single mining action
            print(f"Mining {rock.name}...")
            time.sleep(mining_time)
        
        results = []
        total_ore = 0
        
        for _ in range(count):
            # Determine ore quantity for this attempt
            ore_quantity = 1
            
            # Level-based chance for extra ore
            extra_ore_chance = min(0.3, (mining_level / 100) * 0.3)
            if random.random() < extra_ore_chance:
                ore_quantity += 1
                if random.random() < 0.5:  # 50% chance for a third ore
                    ore_quantity += 1
            
            # 5x ore powerup chance
            if has_5x_ore_chance and random.random() < 0.05:  # 5% chance
                ore_quantity = 5
                if count == 1:  # Only show message for single mining
                    print("You found 5x ore!")
            
            # Create the ore item
            ore_item = Item(rock.ore_name, f"Ore mined from {rock.name}", True)
            
            # Calculate XP
            xp_gained = rock.base_xp * ore_quantity
            
            # Check for easter eggs
            easter_egg = None
            for egg_name, chance in self.easter_eggs.items():
                if random.random() < chance:
                    easter_egg = egg_name
                    print(f"You found a {easter_egg}!")
                    break
            
            results.append((ore_item, xp_gained, easter_egg))
            total_ore += ore_quantity
        
        print(f"You mined a total of {total_ore} {rock.ore_name}.")
        
        return results