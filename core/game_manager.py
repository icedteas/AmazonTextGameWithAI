"""
Game manager for the Text RPG game.
"""
import random
from typing import Dict, List, Optional
from core.player import Player
from core.bank import Bank
from core.shop import Shop
from core.collection_log import CollectionLog
from core.inventory import Item
from skills.mining import MiningSkill
from skills.crafting import CraftingSkill
from skills.magic import MagicSkill

class GameManager:
    """
    Central manager for game mechanics and systems.
    """
    def __init__(self, player: Player):
        """
        Initialize the game manager.
        
        Args:
            player: The player instance
        """
        self.player = player
        self.bank = Bank()
        self.shop = Shop()
        self.collection_log = CollectionLog()
        
        # Initialize skills
        self.mining_skill = MiningSkill()
        self.crafting_skill = CraftingSkill()
        self.magic_skill = MagicSkill()
        
        # Create item cache for quick lookups
        self.item_cache = {}
    
    def start(self) -> None:
        """Start the game and run the main interface."""
        from interfaces.game_interface import GameInterface
        
        interface = GameInterface(self)
        interface.run()
    
    def list_available_rocks(self) -> None:
        """List rocks available to mine at the player's level."""
        mining_level = self.player.skills.get_level("mining")
        available_rocks = self.mining_skill.get_available_rocks(mining_level)
        
        print("\nAvailable rocks to mine:")
        for rock in available_rocks:
            print(f"  {rock.name} (level {rock.level_req}) - Yields {rock.ore_name}")
    
    def mine_rock(self, rock_name: str, count: int = 1) -> None:
        """
        Mine a rock to get ore.
        
        Args:
            rock_name: Name of the rock to mine
            count: Number of mining attempts (1-100)
        """
        mining_level = self.player.skills.get_level("mining")
        equipment_bonuses = self.player.equipment.get_all_bonuses()
        has_faster_mining = self.player.has_active_powerup("faster_mining")
        has_5x_ore_chance = self.player.has_active_powerup("chance_5x_ore")
        
        # Ensure count is within limits
        count = max(1, min(100, count))
        
        results = self.mining_skill.mine_rock(
            rock_name, 
            mining_level, 
            equipment_bonuses,
            has_faster_mining,
            has_5x_ore_chance,
            count
        )
        
        total_xp = 0
        total_ores = 0
        
        for ore_item, xp_gained, easter_egg in results:
            if ore_item:
                # Add ore to inventory
                if self.player.inventory.add_item(ore_item):
                    total_ores += 1
                else:
                    print("Your inventory is full! Some ore falls to the ground.")
                    break  # Stop processing if inventory is full
                
                # Track XP
                total_xp += xp_gained
                
                # Handle easter egg
                if easter_egg:
                    easter_egg_item = Item(easter_egg, f"A rare {easter_egg.lower()}", False)
                    if self.player.inventory.add_item(easter_egg_item):
                        self.collection_log.add_easter_egg(easter_egg)
                    else:
                        print(f"Your inventory is full! The {easter_egg} flies away.")
        
        # Add total XP with potential double XP powerup
        if total_xp > 0:
            xp_multiplier = 2.0 if self.player.has_active_powerup("double_xp") else 1.0
            self.player.skills.add_experience("mining", total_xp, xp_multiplier)
            print(f"Gained {total_xp * xp_multiplier:.0f} Mining XP.")
    
    def list_craftable_items(self) -> None:
        """List items available to craft at the player's level."""
        crafting_level = self.player.skills.get_level("crafting")
        available_items = self.crafting_skill.get_available_items(crafting_level)
        
        print("\nAvailable items to craft:")
        for item in available_items:
            materials_str = ", ".join(f"{qty} {mat}" for mat, qty in item.materials.items())
            print(f"  {item.name} (level {item.level_req}) - Requires: {materials_str}")
    
    def craft_item(self, item_name: str, count: int = 1) -> None:
        """
        Craft an item if the player has the required level and materials.
        
        Args:
            item_name: Name of the item to craft
            count: Number of items to craft (1-100)
        """
        crafting_level = self.player.skills.get_level("crafting")
        
        # Check if the item exists
        item_key = item_name.lower()
        craftable_items = self.crafting_skill.craftable_items
        if item_key not in craftable_items:
            print(f"Unknown item: {item_name}")
            return
        
        # Ensure count is within limits
        count = max(1, min(100, count))
        
        # Check if the player has the materials
        craftable_item = craftable_items[item_key]
        has_materials = True
        material_count = 0
        
        # Calculate how many items can be crafted based on available materials
        for material, quantity_per_item in craftable_item.materials.items():
            available = self.player.inventory.count_item(material)
            required = quantity_per_item * count
            
            if available < required:
                max_craftable = available // quantity_per_item
                if max_craftable == 0:
                    print(f"You don't have enough {material}. Need {quantity_per_item} per item.")
                    has_materials = False
                    break
                else:
                    print(f"You only have enough {material} to craft {max_craftable} items.")
                    count = max_craftable
            
            # Track the material count for the first material (simplified)
            if material_count == 0:
                material_count = available
        
        if has_materials:
            # Remove materials from inventory for all items being crafted
            for material, quantity_per_item in craftable_item.materials.items():
                total_quantity = quantity_per_item * count
                self.player.inventory.remove_item(material, total_quantity)
            
            # Craft the items
            results = self.crafting_skill.craft_item(
                item_name, 
                crafting_level,
                True,  # We already checked materials
                count,
                material_count
            )
            
            total_xp = 0
            crafted_count = 0
            
            for crafted_item, xp_gained, easter_egg in results:
                if crafted_item:
                    # Add item to inventory
                    if self.player.inventory.add_item(crafted_item):
                        crafted_count += 1
                        # Add to collection log
                        self.collection_log.add_crafted_item(item_name)
                        # Track XP
                        total_xp += xp_gained
                    else:
                        print("Your inventory is full! Some crafted items fall to the ground.")
                        break  # Stop processing if inventory is full
                    
                    # Handle easter egg
                    if easter_egg:
                        easter_egg_item = Item(easter_egg, f"A rare {easter_egg.lower()}", False)
                        if self.player.inventory.add_item(easter_egg_item):
                            self.collection_log.add_easter_egg(easter_egg)
                        else:
                            print(f"Your inventory is full! The {easter_egg} flies away.")
            
            # Add total XP with potential double XP powerup
            if total_xp > 0:
                xp_multiplier = 2.0 if self.player.has_active_powerup("double_xp") else 1.0
                self.player.skills.add_experience("crafting", total_xp, xp_multiplier)
                print(f"Gained {total_xp * xp_multiplier:.0f} Crafting XP.")
    
    def list_alchemizable_items(self) -> None:
        """List items that can be alchemized at the player's level."""
        magic_level = self.player.skills.get_level("magic")
        
        # Get items in the player's inventory
        inventory_items = []
        for slot in self.player.inventory.slots:
            if not slot.is_empty():
                inventory_items.append(slot.item.name)
        
        # Filter for alchemizable items
        alchemizable_items = []
        for item_name in inventory_items:
            if self.magic_skill.can_alchemize(item_name, magic_level):
                gold_value = self.magic_skill.get_alchemy_value(item_name)
                alchemizable_items.append((item_name, gold_value))
        
        if not alchemizable_items:
            print("\nYou don't have any items that you can alchemize.")
            return
        
        print("\nItems you can alchemize:")
        for item_name, gold_value in sorted(alchemizable_items, key=lambda x: x[1], reverse=True):
            print(f"  {item_name} - {gold_value} gold")
    
    def alchemize_item(self, item_name: str, count: int = 1) -> None:
        """
        Alchemize an item to get gold.
        
        Args:
            item_name: Name of the item to alchemize
            count: Number of items to alchemize (1-100)
        """
        magic_level = self.player.skills.get_level("magic")
        
        # Ensure count is within limits
        count = max(1, min(100, count))
        
        # Check if the player has the items
        available_count = self.player.inventory.count_item(item_name)
        if available_count == 0:
            print(f"You don't have any {item_name} in your inventory.")
            return
        
        if available_count < count:
            print(f"You only have {available_count} {item_name} in your inventory.")
            count = available_count
        
        # Check if the item can be alchemized
        if not self.magic_skill.can_alchemize(item_name, magic_level):
            print(f"You can't alchemize {item_name} at your Magic level.")
            return
        
        # Remove the items from inventory
        self.player.inventory.remove_item(item_name, count)
        
        # Alchemize the items
        results = self.magic_skill.alchemize(item_name, magic_level, count)
        
        total_gold = 0
        total_xp = 0
        
        for gold, xp_gained, easter_egg in results:
            # Add gold to player
            total_gold += gold
            
            # Track XP
            total_xp += xp_gained
            
            # Handle easter egg
            if easter_egg:
                easter_egg_item = Item(easter_egg, f"A rare {easter_egg.lower()}", False)
                if self.player.inventory.add_item(easter_egg_item):
                    self.collection_log.add_easter_egg(easter_egg)
                else:
                    print(f"Your inventory is full! The {easter_egg} flies away.")
        
        # Add total gold to player
        self.player.add_gold(total_gold)
        
        # Add total XP with potential double XP powerup
        if total_xp > 0:
            xp_multiplier = 2.0 if self.player.has_active_powerup("double_xp") else 1.0
            self.player.skills.add_experience("magic", total_xp, xp_multiplier)
            print(f"Gained {total_xp * xp_multiplier:.0f} Magic XP.")
    
    def deposit_item(self, item_name: str, quantity: int = 1) -> None:
        """
        Deposit an item from inventory to bank.
        
        Args:
            item_name: Name of the item to deposit
            quantity: How many to deposit
        """
        # Check if the player has the item
        if not self.player.inventory.has_item(item_name, quantity):
            print(f"You don't have {quantity} {item_name} in your inventory.")
            return
        
        # Get the item from inventory
        for slot in self.player.inventory.slots:
            if not slot.is_empty() and slot.item.name == item_name:
                item = slot.item
                break
        else:
            print(f"Error finding {item_name} in inventory.")
            return
        
        # Remove from inventory and add to bank
        removed = self.player.inventory.remove_item(item_name, quantity)
        if self.bank.deposit(item, removed):
            print(f"Deposited {removed} {item_name} to your bank.")
        else:
            # If bank is full, return items to inventory
            self.player.inventory.add_item(item, removed)
            print("Your bank is full!")
    
    def withdraw_item(self, item_name: str, quantity: int = 1) -> None:
        """
        Withdraw an item from bank to inventory.
        
        Args:
            item_name: Name of the item to withdraw
            quantity: How many to withdraw
        """
        # Check if the bank has the item
        if not self.bank.has_item(item_name, quantity):
            print(f"You don't have {quantity} {item_name} in your bank.")
            return
        
        # Check if inventory has space
        if self.player.inventory.is_full():
            print("Your inventory is full!")
            return
        
        # Withdraw from bank
        item, withdrawn = self.bank.withdraw(item_name, quantity)
        
        if item and withdrawn > 0:
            # Add to inventory
            if self.player.inventory.add_item(item, withdrawn):
                print(f"Withdrew {withdrawn} {item_name} from your bank.")
            else:
                # If inventory can't fit all items, return remainder to bank
                actual_added = self.player.inventory.count_item(item_name)
                remainder = withdrawn - actual_added
                if remainder > 0:
                    self.bank.deposit(item, remainder)
                    print(f"Withdrew {actual_added} {item_name}. Your inventory is now full.")
    
    def buy_item(self, item_name: str) -> None:
        """
        Buy an item from the shop.
        
        Args:
            item_name: Name of the item to buy
        """
        # Check if the shop has the item
        shop_item = self.shop.get_item(item_name)
        if not shop_item:
            print(f"The shop doesn't sell {item_name}.")
            return
        
        # Check if the player has enough gold
        if not self.player.spend_gold(shop_item.price):
            return
        
        # Handle different types of shop items
        if "Powerup" in shop_item.item.name:
            # Add powerup to bank
            if self.bank.deposit(shop_item.item, 1):
                print(f"Purchased {shop_item.name} for {shop_item.price} gold. It has been added to your bank.")
            else:
                # Refund if bank is full
                self.player.add_gold(shop_item.price)
                print("Your bank is full! Purchase canceled.")
        elif "Cape" in shop_item.name:
            # Check skill level requirement for skill capes
            skill_name = shop_item.name.split()[0].lower()
            required_level = 99
            
            if self.player.skills.get_level(skill_name) < required_level:
                # Refund if level too low
                self.player.add_gold(shop_item.price)
                print(f"You need level {required_level} {skill_name.title()} to purchase this cape.")
                return
            
            # Add cape to inventory or bank
            if not self.player.inventory.is_full():
                self.player.inventory.add_item(shop_item.item, 1)
                print(f"Purchased {shop_item.name} for {shop_item.price} gold.")
            elif self.bank.deposit(shop_item.item, 1):
                print(f"Purchased {shop_item.name} for {shop_item.price} gold. It has been added to your bank.")
            else:
                # Refund if both inventory and bank are full
                self.player.add_gold(shop_item.price)
                print("Your inventory and bank are full! Purchase canceled.")
    
    def equip_item(self, item_name: str) -> None:
        """
        Equip an item from inventory.
        
        Args:
            item_name: Name of the item to equip
        """
        # Check if the player has the item
        if not self.player.inventory.has_item(item_name):
            print(f"You don't have a {item_name} in your inventory.")
            return
        
        # Determine the equipment slot
        slot = None
        if "ring" in item_name.lower():
            slot = "ring"
        elif "pickaxe" in item_name.lower():
            slot = "main_hand"
        elif "chisel" in item_name.lower():
            slot = "off_hand"
        elif "cape" in item_name.lower():
            slot = "cape"
        
        if not slot:
            print(f"{item_name} is not an equippable item.")
            return
        
        # Create equipment item
        from core.equipment import EquipmentItem
        
        # Determine level requirement and bonuses based on tier
        level_req = 1
        bonuses = {"mining_speed": 0.05, "extra_ore_chance": 0.05}
        
        for tier, level in [
            ("bronze", 1), ("iron", 5), ("mithril", 15), ("adamant", 30),
            ("coal", 50), ("rune", 65), ("dragon", 75), ("elite", 85), ("king", 95)
        ]:
            if tier in item_name.lower():
                level_req = level
                bonus_value = 0.05 + (level // 10) * 0.05
                bonuses = {"mining_speed": bonus_value, "extra_ore_chance": bonus_value}
                break
        
        # Check if player meets level requirement
        if self.player.skills.get_level("crafting") < level_req:
            print(f"You need level {level_req} Crafting to equip {item_name}.")
            return
        
        equipment_item = EquipmentItem(
            item_name,
            slot,
            level_req,
            f"A {item_name.lower()} for mining"
        )
        equipment_item.bonuses = bonuses
        
        # Remove from inventory
        self.player.inventory.remove_item(item_name, 1)
        
        # Equip and handle previously equipped item
        old_item = self.player.equipment.equip(equipment_item)
        if old_item:
            if not self.player.inventory.add_item(old_item, 1):
                print(f"Your inventory is full! The {old_item.name} falls to the ground.")
        
        print(f"Equipped {item_name}.")
    
    def unequip_item(self, slot: str) -> None:
        """
        Unequip an item from an equipment slot.
        
        Args:
            slot: The equipment slot to unequip from
        """
        # Check if the slot is valid
        if slot not in self.player.equipment.slots:
            print(f"Invalid equipment slot: {slot}")
            return
        
        # Check if there's an item equipped in the slot
        equipped_item = self.player.equipment.get_equipped(slot)
        if not equipped_item:
            print(f"You don't have anything equipped in your {slot} slot.")
            return
        
        # Check if inventory has space
        if self.player.inventory.is_full():
            print("Your inventory is full! You can't unequip the item.")
            return
        
        # Unequip the item
        item = self.player.equipment.unequip(slot)
        if item:
            self.player.inventory.add_item(item, 1)
            print(f"Unequipped {item.name}.")