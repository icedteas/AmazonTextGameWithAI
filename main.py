#!/usr/bin/env python3
"""
Text RPG Game - Main Entry Point
"""
import os
import sys
import time
from core.player import Player
from core.game_manager import GameManager

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    """Display welcome message and game title."""
    clear_screen()
    print("=" * 60)
    print(" " * 15 + "QUACK THE CODE TEXT ADVENTURE" + " " * 15)
    print("=" * 60)
    print("\nWelcome to Quack The Code Text Adventure!")
    print("In this game, you'll mine resources, craft items, and use magic.")
    print("Collect rare items and fill your collection log as you progress.")
    print("\nLet's begin your adventure!\n")

def get_player_name():
    """Get the player's name from user input."""
    while True:
        name = input("Enter your character's name: ").strip()
        if name and len(name) <= 20:
            return name
        print("Please enter a valid name (1-20 characters).")

def main():
    """Main game loop."""
    display_welcome()
    player_name = get_player_name()
    
    # Create player and game manager
    player = Player(player_name)
    game = GameManager(player)
    
    # Start the game
    game.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user. Goodbye!")
        sys.exit(0)