"""
Unit tests for Coffee Shop Simulator game.
"""
import unittest
from unittest.mock import patch
from coffee_shop_simulator import CoffeeShopSimulator


class CoffeeShopSimulatorTests(unittest.TestCase):
    """Test cases for CoffeeShopSimulator class."""

    def test_convert_to_float(self):
        """Test string conversion to float."""
        test_float = 1.23
        test_string = '1.23'
        self.assertEqual(CoffeeShopSimulator.convert_to_float(test_string), test_float)

    def test_convert_to_float_invalid(self):
        """Test conversion with invalid string returns 0."""
        self.assertEqual(CoffeeShopSimulator.convert_to_float('invalid'), 0)
        self.assertEqual(CoffeeShopSimulator.convert_to_float(''), 0)

    def test_x_of_y_with_numbers(self):
        """Test that x_of_y returns a list of x numbers of y."""
        number_list = [1, 1, 1, 1, 1]
        self.assertEqual(CoffeeShopSimulator.x_of_y(5, 1), number_list)

    def test_x_of_y_with_strings(self):
        """Test that x_of_y returns a list of x strings of y."""
        string_list = ['a', 'a', 'a', 'a']
        self.assertEqual(CoffeeShopSimulator.x_of_y(4, 'a'), string_list)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_initialization(self, mock_input):
        """Test game initialization with proper defaults."""
        game = CoffeeShopSimulator()
        self.assertEqual(game.player_name, 'Test Player')
        self.assertEqual(game.shop_name, 'Test Coffee Shop')
        self.assertEqual(game.day, 1)
        self.assertEqual(game.cash, 100.00)
        self.assertEqual(game.coffee_inventory, 100)
        self.assertEqual(len(game.sales), 0)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_buy_coffee_success(self, mock_input):
        """Test successful coffee purchase."""
        game = CoffeeShopSimulator()
        initial_cash = game.cash
        initial_inventory = game.coffee_inventory
        result = game.buy_coffee('50')
        self.assertTrue(result)
        self.assertEqual(game.cash, initial_cash - 50)
        self.assertEqual(game.coffee_inventory, initial_inventory + 50)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_buy_coffee_insufficient_cash(self, mock_input):
        """Test coffee purchase with insufficient cash."""
        game = CoffeeShopSimulator()
        result = game.buy_coffee('200')
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_buy_coffee_invalid_amount(self, mock_input):
        """Test coffee purchase with invalid amount."""
        game = CoffeeShopSimulator()
        result = game.buy_coffee('invalid')
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_buy_coffee_negative_amount(self, mock_input):
        """Test coffee purchase with negative amount."""
        game = CoffeeShopSimulator()
        result = game.buy_coffee('-10')
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_increment_day(self, mock_input):
        """Test day counter increments correctly."""
        game = CoffeeShopSimulator()
        initial_day = game.day
        game.increment_day()
        self.assertEqual(game.day, initial_day + 1)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_make_temp_distribution(self, mock_input):
        """Test temperature distribution creation."""
        game = CoffeeShopSimulator()
        self.assertEqual(len(game.temps), game.SERIES_DENSITY)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_daily_sales(self, mock_input):
        """Test daily sales calculation."""
        game = CoffeeShopSimulator()
        temperature = 50
        advertising = 10
        cup_price = 2
        sales = game.daily_sales(temperature, advertising, cup_price)
        self.assertGreaterEqual(sales, 0)
        self.assertLessEqual(sales, game.coffee_inventory)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_daily_sales_exceeds_inventory(self, mock_input):
        """Test sales cannot exceed inventory."""
        game = CoffeeShopSimulator()
        game.coffee_inventory = 5
        temperature = 20
        advertising = 100
        cup_price = 1
        sales = game.daily_sales(temperature, advertising, cup_price)
        self.assertLessEqual(sales, 5)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_simulate(self, mock_input):
        """Test simulate method records sales data."""
        game = CoffeeShopSimulator()
        initial_sales_count = len(game.sales)
        cups_sold = game.simulate(50, 10, 2)
        self.assertEqual(len(game.sales), initial_sales_count + 1)
        self.assertGreaterEqual(cups_sold, 0)

    @patch('builtins.input', side_effect=['Test Player', 'Test Coffee Shop'])
    def test_weather_property(self, mock_input):
        """Test weather property returns valid temperature."""
        game = CoffeeShopSimulator()
        temperature = game.weather
        self.assertGreaterEqual(temperature, game.TEMP_MIN)
        self.assertLessEqual(temperature, game.TEMP_MAX)


if __name__ == '__main__':
    unittest.main()