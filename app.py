"""
Coffee Shop Simulator - Web Application

Flask web server providing a modern web interface for the coffee shop simulator game.
"""
from flask import Flask, render_template, jsonify, request, session
from coffee_shop_simulator import CoffeeShopSimulator
import pickle
import secrets
import random
from pathlib import Path
from typing import Dict, Any

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store active game sessions in memory
games: Dict[str, CoffeeShopSimulator] = {}


class WebCoffeeShopSimulator(CoffeeShopSimulator):
    """
    Extended version of CoffeeShopSimulator for web interface.
    Removes interactive prompts and allows programmatic initialization.
    """

    def __init__(self, player_name: str = None, shop_name: str = None) -> None:
        """Initialize game without interactive prompts."""
        self.player_name = player_name or "Player"
        self.shop_name = shop_name or "Coffee Shop"
        self.day = 1
        self.cash = 100.00
        self.coffee_inventory = 100
        self.sales = []
        self.temps = self.make_temp_distribution()


@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')


@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new game session."""
    data = request.json
    player_name = data.get('player_name', 'Player')
    shop_name = data.get('shop_name', 'Coffee Shop')

    # Create new game
    game = WebCoffeeShopSimulator(player_name, shop_name)

    # Generate session ID
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)

    session_id = session['session_id']
    games[session_id] = game

    return jsonify({
        'success': True,
        'message': f'Welcome to {shop_name}!',
        'game_state': get_game_state(game)
    })


@app.route('/api/game-state', methods=['GET'])
def game_state():
    """Get current game state."""
    session_id = session.get('session_id')
    if not session_id or session_id not in games:
        return jsonify({'error': 'No active game session'}), 404

    game = games[session_id]
    return jsonify(get_game_state(game))


@app.route('/api/play-day', methods=['POST'])
def play_day():
    """Process one day of gameplay."""
    session_id = session.get('session_id')
    if not session_id or session_id not in games:
        return jsonify({'error': 'No active game session'}), 404

    game = games[session_id]
    data = request.json

    cup_price = float(data.get('cup_price', 0))
    coffee_to_buy = int(data.get('coffee_to_buy', 0))
    advertising = float(data.get('advertising', 0))

    # Validate inputs
    if cup_price <= 0:
        return jsonify({'error': 'Price must be positive'}), 400

    # Buy coffee if requested
    buy_result = None
    if coffee_to_buy > 0:
        if coffee_to_buy > game.cash:
            buy_result = {'success': False, 'message': 'Not enough cash to buy coffee'}
        else:
            game.coffee_inventory += coffee_to_buy
            game.cash -= coffee_to_buy
            buy_result = {'success': True, 'message': f'Bought {coffee_to_buy} units of coffee'}

    # Deduct advertising cost
    if advertising > game.cash:
        return jsonify({'error': 'Not enough cash for advertising'}), 400

    game.cash -= advertising

    # Get weather
    temperature = game.weather

    # Simulate sales
    cups_sold = game.simulate(temperature, advertising, cup_price)
    gross_profit = cups_sold * cup_price

    # Add profit
    game.cash += gross_profit

    # Subtract inventory
    game.coffee_inventory -= cups_sold

    # Check game over
    game_over = game.cash < 0

    # Increment day
    if not game_over:
        game.increment_day()

    # Prepare response
    result = {
        'success': True,
        'day_result': {
            'temperature': temperature,
            'cups_sold': cups_sold,
            'gross_profit': round(gross_profit, 2),
            'buy_result': buy_result
        },
        'game_state': get_game_state(game),
        'game_over': game_over,
        'message': 'Game Over! You ran out of cash.' if game_over else None
    }

    return jsonify(result)


@app.route('/api/save-game', methods=['POST'])
def save_game():
    """Save current game state."""
    session_id = session.get('session_id')
    if not session_id or session_id not in games:
        return jsonify({'error': 'No active game session'}), 404

    game = games[session_id]

    try:
        with open(CoffeeShopSimulator.SAVE_FILE, mode='wb') as f:
            pickle.dump(game, f)
        return jsonify({'success': True, 'message': 'Game saved successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to save game: {str(e)}'}), 500


@app.route('/api/load-game', methods=['POST'])
def load_game():
    """Load saved game state."""
    if not Path(CoffeeShopSimulator.SAVE_FILE).is_file():
        return jsonify({'error': 'No saved game found'}), 404

    try:
        with open(CoffeeShopSimulator.SAVE_FILE, mode='rb') as f:
            game = pickle.load(f)

        if 'session_id' not in session:
            session['session_id'] = secrets.token_hex(16)

        session_id = session['session_id']
        games[session_id] = game

        return jsonify({
            'success': True,
            'message': 'Game loaded successfully',
            'game_state': get_game_state(game)
        })
    except Exception as e:
        return jsonify({'error': f'Failed to load game: {str(e)}'}), 500


def get_game_state(game: WebCoffeeShopSimulator) -> Dict[str, Any]:
    """Extract game state as dictionary."""
    return {
        'player_name': game.player_name,
        'shop_name': game.shop_name,
        'day': game.day,
        'cash': round(game.cash, 2),
        'coffee_inventory': game.coffee_inventory,
        'total_sales': len(game.sales),
        'sales_history': game.sales[-10:] if game.sales else []  # Last 10 days
    }


if __name__ == '__main__':
    print("🎮 Coffee Shop Simulator Web Server")
    print("📱 Open your browser to: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
