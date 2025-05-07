"""
Game interface for the Text RPG game.
"""
import os
import time
from typing import List, Dict, Optional

class GameInterface:
    """
    Handles user interface and command processing for the game.
    """
    def __init__(self, game_manager):
        """
        Initialize the game interface.
        
        Args:
            game_manager: The game manager instance
        """
        self.game_manager = game_manager
        self.commands = self._initialize_commands()
        self.current_menu = "main"
        self.previous_menu = None
    
    def _initialize_commands(self) -> Dict[str, Dict[str, str]]:
        """
        Initialize available commands for different menus.
        
        Returns:
            Dict[str, Dict[str, str]]: Dictionary of menu name to commands
        """
        return {
            "main": {
                "status": "Show your player status",
                "skills": "Show your skills and levels",
                "inventory": "Show your inventory",
                "equipment": "Show your equipped items",
                "mine": "Go mining for ores",
                "craft": "Craft items from ores",
                "magic": "Use magic skills",
                "bank": "Access your bank",
                "shop": "Visit the shop",
                "collection": "View your collection log",
                "help": "Show available commands",
                "quit": "Quit the game"
            },
            "mining": {
                "list": "List available rocks to mine",
                "mine <rock>": "Mine a specific rock (e.g., 'mine bronze')",
                "mine <rock> <count>": "Mine multiple rocks (e.g., 'mine bronze 50')",
                "back": "Return to main menu",
                "help": "Show available commands"
            },
            "crafting": {
                "list": "List available items to craft",
                "craft <item>": "Craft a specific item (e.g., 'craft bronze pickaxe')",
                "craft <item> <count>": "Craft multiple items (e.g., 'craft bronze ring 10')",
                "back": "Return to main menu",
                "help": "Show available commands"
            },
            "magic": {
                "list": "List items you can alchemize",
                "alch <item>": "Alchemize an item for gold (e.g., 'alch bronze ring')",
                "alch <item> <count>": "Alchemize multiple items (e.g., 'alch bronze ring 5')",
                "back": "Return to main menu",
                "help": "Show available commands"
            },
            "bank": {
                "list": "List items in your bank",
                "deposit <item> [amount]": "Deposit an item into your bank",
                "withdraw <item> [amount]": "Withdraw an item from your bank",
                "back": "Return to main menu",
                "help": "Show available commands"
            },
            "shop": {
                "list": "List items available in the shop",
                "buy <item>": "Buy an item from the shop",
                "back": "Return to main menu",
                "help": "Show available commands"
            },
            "equipment": {
                "equip <item>": "Equip an item from your inventory",
                "unequip <slot>": "Unequip an item (ring, main_hand, off_hand, cape)",
                "back": "Return to main menu",
                "help": "Show available commands"
            }
        }
    
    def standardize_input(self, text):
        """Standardize input by converting to lowercase."""
        return text.strip().lower()
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self) -> None:
        """Display the game header with current menu."""
        self.clear_screen()
        print("=" * 60)
        print(f" QUACK THE CODE TEXT ADVENTURE - {self.current_menu.upper()} MENU")
        print("=" * 60)
        
        # Show basic player info in header
        player = self.game_manager.player
        print(f"Player: {player.name} | Gold: {player.gold} | Mining: {player.skills.get_level('mining')} | "
              f"Crafting: {player.skills.get_level('crafting')} | Magic: {player.skills.get_level('magic')}")
        print("-" * 60)
    
    def display_help(self) -> None:
        """Display available commands for the current menu."""
        print(f"\nAvailable commands in {self.current_menu} menu:")
        
        for cmd, desc in self.commands[self.current_menu].items():
            print(f"  {cmd:<20} - {desc}")
    
    def change_menu(self, menu_name: str) -> None:
        """
        Change to a different menu.
        
        Args:
            menu_name: Name of the menu to change to
        """
        if menu_name in self.commands:
            self.previous_menu = self.current_menu
            self.current_menu = menu_name
            self.display_header()
            print(f"Entered {menu_name} menu. Type 'help' for available commands.")
        else:
            print(f"Invalid menu: {menu_name}")
    
    def go_back(self) -> None:
        """Go back to the previous menu."""
        if self.previous_menu:
            temp = self.current_menu
            self.current_menu = self.previous_menu
            self.previous_menu = temp
            self.display_header()
            print(f"Returned to {self.current_menu} menu. Type 'help' for available commands.")
        else:
            print("Cannot go back further.")
    
    def process_command(self, command: str) -> bool:
        """
        Process a user command.
        
        Args:
            command: The command to process
            
        Returns:
            bool: True to continue the game, False to quit
        """
        command = self.standardize_input(command)
        
        if not command:
            return True
        
        # Common commands across all menus
        if command == "help":
            self.display_help()
            return True
        elif command == "quit":
            return False
        elif command == "back":
            self.go_back()
            return True
        
        # Process menu-specific commands
        if self.current_menu == "main":
            return self._process_main_menu(command)
        elif self.current_menu == "mining":
            return self._process_mining_menu(command)
        elif self.current_menu == "crafting":
            return self._process_crafting_menu(command)
        elif self.current_menu == "magic":
            return self._process_magic_menu(command)
        elif self.current_menu == "bank":
            return self._process_bank_menu(command)
        elif self.current_menu == "shop":
            return self._process_shop_menu(command)
        elif self.current_menu == "equipment":
            return self._process_equipment_menu(command)
        
        print(f"Unknown command: {command}")
        return True
    
    def _process_main_menu(self, command: str) -> bool:
        """Process commands in the main menu."""
        if command == "status":
            print("\n" + self.game_manager.player.get_status())
        elif command == "skills":
            print("\n" + self.game_manager.player.toggle_skills_interface())
        elif command == "inventory":
            print("\n" + self.game_manager.player.inventory.display())
        elif command == "equipment":
            self.change_menu("equipment")
            print("\n" + self.game_manager.player.equipment.display())
        elif command == "mine":
            self.change_menu("mining")
        elif command == "craft":
            self.change_menu("crafting")
        elif command == "magic":
            self.change_menu("magic")
        elif command == "bank":
            self.change_menu("bank")
        elif command == "shop":
            self.change_menu("shop")
        elif command == "collection":
            print("\n" + self.game_manager.collection_log.display())
        else:
            print(f"Unknown command: {command}")
        
        return True
    
    def _process_mining_menu(self, command: str) -> bool:
        """Process commands in the mining menu."""
        if command == "list":
            self.game_manager.list_available_rocks()
        elif command.startswith("mine "):
            parts = command[5:].strip().split()
            if len(parts) >= 1:
                rock_name = parts[0]
                count = 1
                
                # Check if a count was provided
                if len(parts) >= 2 and parts[1].isdigit():
                    count = int(parts[1])
                    count = max(1, min(100, count))  # Limit to 1-100
                
                # Ask for confirmation if mining multiple rocks
                if count > 1:
                    confirm = input(f"Mine {count} {rock_name} rocks? (y/n): ").strip().lower()
                    if confirm != 'y':
                        print("Mining cancelled.")
                        return True
                
                self.game_manager.mine_rock(rock_name, count)
            else:
                print("Please specify a rock to mine.")
        else:
            print(f"Unknown mining command: {command}")
        
        return True
    
    def _process_crafting_menu(self, command: str) -> bool:
        """Process commands in the crafting menu."""
        if command == "list":
            self.game_manager.list_craftable_items()
        elif command.startswith("craft "):
            parts = command[6:].strip().split()
            if len(parts) >= 1:
                # Handle multi-word item names with count at the end
                if len(parts) >= 2 and parts[-1].isdigit():
                    item_name = " ".join(parts[:-1])
                    count = int(parts[-1])
                    count = max(1, min(100, count))  # Limit to 1-100
                else:
                    item_name = " ".join(parts)
                    count = 1
                
                # Ask for confirmation if crafting multiple items
                if count > 1:
                    confirm = input(f"Craft {count} {item_name}? (y/n): ").strip().lower()
                    if confirm != 'y':
                        print("Crafting cancelled.")
                        return True
                
                self.game_manager.craft_item(item_name, count)
            else:
                print("Please specify an item to craft.")
        else:
            print(f"Unknown crafting command: {command}")
        
        return True
    
    def _process_magic_menu(self, command: str) -> bool:
        """Process commands in the magic menu."""
        if command == "list":
            self.game_manager.list_alchemizable_items()
        elif command.startswith("alch "):
            parts = command[5:].strip().split()
            if len(parts) >= 1:
                # Handle multi-word item names with count at the end
                if len(parts) >= 2 and parts[-1].isdigit():
                    item_name = " ".join(parts[:-1])
                    count = int(parts[-1])
                    count = max(1, min(100, count))  # Limit to 1-100
                else:
                    item_name = " ".join(parts)
                    count = 1
                
                # Ask for confirmation if alchemizing multiple items
                if count > 1:
                    confirm = input(f"Alchemize {count} {item_name}? (y/n): ").strip().lower()
                    if confirm != 'y':
                        print("Alchemizing cancelled.")
                        return True
                
                self.game_manager.alchemize_item(item_name, count)
            else:
                print("Please specify an item to alchemize.")
        else:
            print(f"Unknown magic command: {command}")
        
        return True
    
    def _process_bank_menu(self, command: str) -> bool:
        """Process commands in the bank menu."""
        if command == "list":
            print("\n" + self.game_manager.bank.display())
        elif command.startswith("deposit "):
            parts = command[8:].strip().split()
            item_name = " ".join(parts[:-1]) if len(parts) > 1 and parts[-1].isdigit() else " ".join(parts)
            amount = int(parts[-1]) if len(parts) > 1 and parts[-1].isdigit() else 1
            self.game_manager.deposit_item(item_name, amount)
        elif command.startswith("withdraw "):
            parts = command[9:].strip().split()
            item_name = " ".join(parts[:-1]) if len(parts) > 1 and parts[-1].isdigit() else " ".join(parts)
            amount = int(parts[-1]) if len(parts) > 1 and parts[-1].isdigit() else 1
            self.game_manager.withdraw_item(item_name, amount)
        else:
            print(f"Unknown bank command: {command}")
        
        return True
    
    def _process_shop_menu(self, command: str) -> bool:
        """Process commands in the shop menu."""
        if command == "list":
            print("\n" + self.game_manager.shop.display())
        elif command.startswith("buy "):
            item_name = command[4:].strip()
            self.game_manager.buy_item(item_name)
        else:
            print(f"Unknown shop command: {command}")
        
        return True
    
    def _process_equipment_menu(self, command: str) -> bool:
        """Process commands in the equipment menu."""
        if command.startswith("equip "):
            item_name = command[6:].strip()
            self.game_manager.equip_item(item_name)
        elif command.startswith("unequip "):
            slot = command[8:].strip()
            self.game_manager.unequip_item(slot)
        else:
            print(f"Unknown equipment command: {command}")
        
        return True
    
    def run(self) -> None:
        """Run the main interface loop."""
        self.display_header()
        print("Welcome to the Text RPG Adventure! Type 'help' for available commands.")
        
        running = True
        while running:
            try:
                command = input("\n> ").strip()
                running = self.process_command(command)
            except KeyboardInterrupt:
                print("\nExiting game...")
                running = False
            except Exception as e:
                print(f"Error: {e}")
        
        print("Thanks for playing!")