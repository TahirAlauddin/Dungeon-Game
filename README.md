# Dungeon Game

A text-based adventure game set in a mysterious dungeon, featuring dynamic gameplay and extensive use of Object-Oriented Programming principles.

## Overview

Explore a labyrinth of rooms, fight monsters, collect items, and find your way to freedom in this engaging terminal-based game. Your choices and strategy will determine your fate!

## Features

- **Dynamic World**: Navigate through various interconnected rooms
- **Player Management**: Manage your inventory, resources, and weapons
- **Combat System**: Engage in battles with different types of monsters
- **Item Collection**: Pick up, use, and drop various items throughout the dungeon
- **NPC Interaction**: Interact with non-player characters like the Dwarf
- **Multiple Endings**: Your choices influence the outcome of the game

## Computer Science Concepts Used

1. **Object-Oriented Programming (OOP)**:
   - Extensive use of classes (e.g., `Game`, `Room`, `Player`, `Monster`)
   - Inheritance (e.g., `Monster` types inheriting from a base class)
   - Encapsulation of data and behaviors within classes

2. **Data Structures**:
   - Lists for storing items, weapons, and monsters
   - Dictionaries for mapping rooms and exits

3. **Algorithms**:
   - Randomization for item and monster placement
   - Combat logic for player-monster interactions

4. **File I/O**: (If implemented) Saving and loading game states

5. **Exception Handling**: Custom exceptions for game-specific scenarios

6. **Command Pattern**: Implementation of various game commands

7. **Factory Pattern**: (If implemented) For creating different types of items or monsters

8. **State Management**: Tracking game state, player status, and room conditions

9. **Modularity**: Separation of concerns into different classes and files

10. **Resource Management**: Player inventory system with weight constraints

11. **Graph Theory**: Room connections forming a graph-like structure

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dungeon-game.git
   ```
2. Navigate to the game directory:
   ```
   cd dungeon-game
   ```
3. Run the game:
   ```
   python game.py
   ```

## How to Play

- Use text commands to navigate and interact with the game world
- Common commands: 'go', 'pick', 'drop', 'fight', 'status', 'quit'
- Explore rooms, collect items, and fight monsters to progress
- Find the key and reach the exit room to win!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
