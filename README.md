# Quack The Code Text Adventure

A text-based RPG game with mining, crafting, and magic skills.

## Features

- **Player System**:
  - Customizable player name
  - Experience levels for different skills
  - 28-slot inventory system
  - Equipment slots (ring, main hand, off hand, cape)

- **Skills**:
  - **Mining**: Mine various rocks to obtain ores
  - **Crafting**: Create equipment from ores
  - **Magic**: Alchemize items for gold

- **Game Systems**:
  - **Bank**: Store up to 1000 stacks of items
  - **Shop**: Purchase powerups and skill capes
  - **Collection Log**: Track crafted items and rare finds
  - **Idle Features**: Batch processing for mining, crafting, and magic (up to 100 at once)

- **Easter Eggs**:
  - Rare pets and creatures to discover while skilling

## How to Play

1. Run the game: `python main.py`
2. Enter your character name
3. Use commands to navigate the game:
   - Type `help` to see available commands
   - Use `mine`, `craft`, and `magic` to train your skills
   - Visit the `bank` to store your items
   - Check the `shop` for upgrades

## Game Commands

### Main Menu
- `status` - Show your player status
- `skills` - Show your skills and levels
- `inventory` - Show your inventory
- `equipment` - Show your equipped items
- `mine` - Go mining for ores
- `craft` - Craft items from ores
- `magic` - Use magic skills
- `bank` - Access your bank
- `shop` - Visit the shop
- `collection` - View your collection log
- `help` - Show available commands
- `quit` - Quit the game

### Mining Menu
- `list` - List available rocks to mine
- `mine <rock>` - Mine a specific rock (e.g., 'mine bronze')
- `mine <rock> <count>` - Mine multiple rocks (e.g., 'mine bronze 50')
- `back` - Return to main menu
- `help` - Show available commands

### Crafting Menu
- `list` - List available items to craft
- `craft <item>` - Craft a specific item (e.g., 'craft bronze pickaxe')
- `craft <item> <count>` - Craft multiple items (e.g., 'craft bronze ring 10')
- `back` - Return to main menu
- `help` - Show available commands

### Magic Menu
- `list` - List items you can alchemize
- `alch <item>` - Alchemize an item for gold (e.g., 'alch bronze ring')
- `alch <item> <count>` - Alchemize multiple items (e.g., 'alch bronze ring 5')
- `back` - Return to main menu
- `help` - Show available commands

### Bank Menu
- `list` - List items in your bank
- `deposit <item> [amount]` - Deposit an item into your bank
- `withdraw <item> [amount]` - Withdraw an item from your bank
- `back` - Return to main menu
- `help` - Show available commands

### Shop Menu
- `list` - List items available in the shop
- `buy <item>` - Buy an item from the shop
- `back` - Return to main menu
- `help` - Show available commands

### Equipment Menu
- `equip <item>` - Equip an item from your inventory
- `unequip <slot>` - Unequip an item (ring, main_hand, off_hand, cape)
- `back` - Return to main menu
- `help` - Show available commands