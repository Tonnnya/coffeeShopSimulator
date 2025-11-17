# Import needed modules
import pickle
import random
import re
from typing import List, Dict, Any, Optional
import numpy


class CoffeeShopSimulator:
    """
    A coffee shop business simulator game.

    Players manage a coffee shop by making daily decisions about pricing,
    advertising, and inventory. The game simulates sales based on weather,
    advertising effectiveness, and pricing strategy.

    Attributes:
        TEMP_MIN (int): Minimum temperature in Fahrenheit
        TEMP_MAX (int): Maximum temperature in Fahrenheit
        SERIES_DENSITY (int): Number of points in temperature distribution
        SAVE_FILE (str): Path to save game file
    """
    # Min & max temperatures
    TEMP_MIN = 20
    TEMP_MAX = 90

    # Length of temperature list
    # {higher produces more realistic curve}
    SERIES_DENSITY = 300

    # Save game file
    SAVE_FILE = 'savegame.dat'

    # Faux temp distributions. We'll do this better
    # later with a bell curve, but for now a quick hack

    def __init__(self) -> None:
        """
        Initialize a new coffee shop simulator game.

        Sets up initial game state with starting cash, inventory, and prompts
        the player for their name and shop name.
        """
        # Get name and coffee shop name
        print("Let's collect some information before we start the game.\n")
        self.player_name: str = self.prompt('What is your name?', True)
        self.shop_name: str = self.prompt('What do you want to name your coffee shop?', True)

        # Current day number
        self.day: int = 1

        # Cash on hand at start
        self.cash: float = 100.00

        # Inventory at start
        self.coffee_inventory: int = 100

        # Sales list
        self.sales: List[Dict[str, Any]] = []

        # Possible temperatures
        self.temps: numpy.ndarray = self.make_temp_distribution()

    def run(self) -> None:
        """
        Run the main game loop.

        Handles daily operations including getting weather, prompting for
        decisions, simulating sales, and updating game state. Continues
        until player quits or runs out of cash.
        """
        print(f"\nOk, let's get started. Have fun!")

        # The main game loop
        running = True
        while running:
            # Display the day and add a 'fancy' text effect
            self.day_header()

            # Get the weather
            temperature = self.weather

            # Display the cash and weather
            self.daily_stats(temperature)

            # Get price of a cup of coffee
            response = self.prompt('What do you want to charge per cup of coffee? (type exit to quit)')
            if re.search('^exit', response, re.IGNORECASE):
                running = False
                continue
            else:
                cup_price = self.convert_to_float(response)
                if cup_price <= 0:
                    print('Invalid price. Please enter a positive number.')
                    continue

            # Do they want to buy more coffee inventory?
            print("\nIt costs $1 for the necessary inventory to make a cup of coffee.")
            response = self.prompt(
                'Want to buy more coffee? (hit Enter for none or enter number)', False)

            if response:
                if not self.buy_coffee(response):
                    print('Could not buy additional coffee.')

            # Get price of a cup of coffee
            print('\nYou can buy advertising to help promote sale')
            advertising = self.prompt('How much do you want to spend on advertising (0 for none)', False)

            # Convert adv into a float
            advertising = self.convert_to_float(advertising)

            # Deduct adv from cash on hand
            self.cash -= advertising

            # Simulate today's sales
            cups_sold = self.simulate(temperature, advertising, cup_price)
            gross_profit = cups_sold * cup_price

            # Display the results
            print(f'You sold {str(cups_sold)} cups of coffee today.')
            print(f'You made $ {str(gross_profit)}.')

            # Add the profit to our coffers
            self.cash += gross_profit

            # Subtrack inventory
            self.coffee_inventory -= cups_sold

            if self.cash < 0:
                print('\n:( GAME OVER! You ran out of cash.')
                running = False
                continue

            # Before we loop around, add a day
            self.increment_day()

            with open(self.SAVE_FILE, mode='wb') as f:
                pickle.dump(self, f)

    def simulate(self, temperature: float, advertising: float, cup_price: float) -> int:
        """
        Simulate one day of coffee shop sales.

        Args:
            temperature: Current temperature in Fahrenheit
            advertising: Amount spent on advertising
            cup_price: Price per cup of coffee

        Returns:
            Number of cups sold today
        """
        # Find out how many cups were sold
        cups_sold = self.daily_sales(temperature, advertising, cup_price)

        # Save the sales data for today
        self.sales.append({
            'day': self.day,
            'coffee_inv': self.coffee_inventory,
            'advertising': advertising,
            'temp': temperature,
            'cup_price': cup_price,
            'cups_sold': cups_sold
        })

        # We technically don't need this, but why make the next step
        # read from the sales list when we have the data right here
        return cups_sold

    def buy_coffee(self, amount: str) -> bool:
        """
        Purchase additional coffee inventory.

        Args:
            amount: String representation of amount to purchase

        Returns:
            True if purchase successful, False otherwise
        """
        try:
            i_amount = int(amount)
        except ValueError:
            return False

        if i_amount <= 0:
            return False

        if i_amount <= self.cash:
            self.coffee_inventory += i_amount
            self.cash -= i_amount
            return True
        else:
            return False

    def make_temp_distribution(self) -> numpy.ndarray:
        """
        Create a realistic temperature distribution using a bell curve.

        Returns:
            Array of temperature values following a normal distribution
        """
        # Create series of numbers between TEMP_MIN and TEMP_MAX
        series = numpy.linspace(self.TEMP_MIN, self.TEMP_MAX, self.SERIES_DENSITY)

        # Obtain mean and standard deviation and return from the series
        mean = numpy.mean(series)
        std_dev = numpy.std(series)

        # Calculate probability density and return the list it creates
        return (numpy.pi * std_dev) * numpy.exp(-0.5 * ((series - mean) / std_dev) ** 2)

    def increment_day(self) -> None:
        """Increment the day counter."""
        self.day += 1

    def daily_stats(self, temperature: float) -> None:
        """
        Display daily statistics.

        Args:
            temperature: Current temperature in Fahrenheit
        """
        print(f'You have ${self.cash:.2f} cash on hand and the temperature is '
              f'{temperature:.0f}°F.')
        print(f'You have enough coffee on hand to make {self.coffee_inventory} cups.\n')

    def day_header(self) -> None:
        """Display the header for the current day."""
        print(f'\n------| Day {self.day} @{self.shop_name} |------')

    def daily_sales(self, temperature: float, advertising: float, cup_price: float) -> int:
        """
        Calculate daily coffee sales based on multiple factors.

        The algorithm considers:
        - Temperature: Colder weather increases coffee demand
        - Advertising: Random effectiveness between 20-80%
        - Price: Higher prices reduce sales
        - Inventory: Cannot sell more than available stock

        Args:
            temperature: Current temperature in Fahrenheit
            advertising: Amount spent on advertising
            cup_price: Price per cup of coffee

        Returns:
            Number of cups sold
        """
        # Randomize advertising effectiveness
        adv_coefficient = random.randint(20, 80) / 100

        # Higher priced coffee doesn't sell as well
        price_coefficient = int((cup_price * (random.randint(50, 250) / 100)))

        # Run the sales figures!
        sales = int((self.TEMP_MAX - temperature) * (advertising * adv_coefficient))

        # If price is too high, we don't sell anything
        if price_coefficient > sales:
            sales = 0
        else:
            sales -= price_coefficient

        if sales > self.coffee_inventory:
            sales = self.coffee_inventory
            print(f'You would have sold more coffee but you ran out. Be sure to buy additional inventory.')

        return sales

    @property
    def weather(self) -> int:
        """
        Get a random temperature from the distribution.

        Returns:
            Temperature in Fahrenheit
        """
        # Generate a random temperature between 20 and 90
        # We'll consider seasons later on, but this is good enough for now
        return int(random.choice(self.temps))

    @staticmethod
    def prompt(display: str = 'Please input a string', require: bool = True) -> str:
        """
        Prompt user for input with optional validation.

        Args:
            display: Prompt message to show user
            require: If True, keeps prompting until non-empty input received

        Returns:
            User input string
        """
        if require:
            s = False
            while not s:
                s = input(f'{display} ')
        else:
            s = input(f'{display} ')
        return s

    @staticmethod
    def convert_to_float(s: str) -> float:
        """
        Safely convert string to float.

        Args:
            s: String to convert

        Returns:
            Float value, or 0 if conversion fails
        """
        # If conversion fails, assign 0 to it
        try:
            f = float(s)
        except ValueError:
            f = 0
        return f

    @staticmethod
    def x_of_y(x: int, y: Any) -> List[Any]:
        """
        Create a list containing x copies of y.

        Args:
            x: Number of copies
            y: Value to copy

        Returns:
            List containing x copies of y
        """
        num_list = []
        # Return a list of x copies of y
        for i in range(x):
            num_list.append(y)
        return num_list
