# Import all functions from the utility module
import pickle
import re
from pathlib import Path

# Import the game class from the coffee_shop_simulator module
from coffee_shop_simulator import CoffeeShopSimulator

# Print welcome message
print("Coffee Shop Simulator 2024, Version 1.00")
print("Copyright (C) 2024 Tonnnya, All Rights Reserved.\n")

# If save file exists, see if the player wants to load it
run_game = True
if Path(CoffeeShopSimulator.SAVE_FILE).is_file():
    # Save game exists, do they want to load it?
    response = CoffeeShopSimulator.prompt("There's a saved game. Do you want to load it? Y/N", True)
    if re.search('y', response, re.IGNORECASE):
        # Load the game and run
        with open(CoffeeShopSimulator.SAVE_FILE, mode='rb') as f:
            game = pickle.load(f)
            game.run()
            # We don't need to run the game again
            run_game = False
    else:
        print(f"HINT: If you don't want to see this prompt again, remove the {CoffeeShopSimulator.SAVE_FILE} file.\n")

if run_game:
    # Create the game object and run it!
    game = CoffeeShopSimulator()
    game.run()

# Say goodbay!
print(f'\nThank you for playing. Have a great rest of your day!\n')



