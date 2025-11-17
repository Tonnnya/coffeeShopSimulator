[![Python CI](https://github.com/Tonnnya/coffeeShopSimulator/actions/workflows/blank.yml/badge.svg)](https://github.com/Tonnnya/coffeeShopSimulator/actions/workflows/blank.yml)

# Coffee Shop Simulator

A text-based business simulation game where you manage your own coffee shop! Make strategic decisions about pricing, advertising, and inventory management to maximize profits and keep your shop running.

## 📖 Description

In Coffee Shop Simulator, you start with $100 in cash and 100 units of coffee inventory. Each day, you'll face new challenges:
- Dynamic weather conditions (temperature affects sales)
- Pricing strategy decisions
- Inventory management
- Advertising budget allocation

The game features a realistic sales simulation that factors in temperature, advertising effectiveness, and pricing to determine your daily sales. Make smart decisions to grow your business!

## 🎮 Features

- **Interactive gameplay loop** with daily decision-making
- **Dynamic weather system** (temperatures ranging from 20°F to 90°F)
- **Sales simulation** based on multiple variables
- **Persistent game saves** - continue your progress anytime
- **Business strategy** - balance pricing, advertising, and inventory

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Tonnnya/coffeeShopSimulator.git
cd coffeeShopSimulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

## 🎯 How to Play

1. **Start the game** - Enter your name and coffee shop name
2. **Daily decisions:**
   - Set the price per cup of coffee
   - Buy additional inventory ($1 per cup's worth)
   - Allocate advertising budget
3. **Watch your results** - See how many cups you sold and your profit
4. **Manage your finances** - Don't let your cash run out!
5. **Type 'exit'** when setting cup price to quit the game

### Tips for Success

- ☕ Higher temperatures generally mean higher sales
- 💰 Price too high? Customers won't buy
- 📢 Advertising helps, but isn't always worth the cost
- 📦 Keep enough inventory to meet demand
- 💸 Watch your cash flow - going negative ends the game!

## 🧪 Running Tests

```bash
python -m pytest coffee_shop_simulator_tests.py -v
```

## 📊 Game Mechanics

The sales algorithm considers:
- **Temperature**: Colder weather drives more coffee sales
- **Advertising**: Random effectiveness between 20-80%
- **Price**: Higher prices reduce demand
- **Inventory**: You can't sell more than you have in stock

## 🛠️ Development

### Project Structure

```
coffeeShopSimulator/
├── coffee_shop_simulator.py    # Main game logic and CoffeeShopSimulator class
├── main.py                      # Entry point and save/load functionality
├── utilities.py                 # Utility functions (deprecated)
├── coffee_shop_simulator_tests.py  # Unit tests
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Dependencies

- `numpy==2.1.2` - For realistic temperature distribution calculations

## 📝 License

Copyright (C) 2024 Tonnnya, All Rights Reserved

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the game!

## 🎓 Learning Objectives

This project demonstrates:
- Object-oriented programming in Python
- Game loop architecture
- File I/O with pickle serialization
- Random number generation and probability
- Input validation and error handling
- Unit testing
- CI/CD with GitHub Actions

