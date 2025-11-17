// Coffee Shop Simulator - Game Logic

let currentGameState = null;

// Screen Management
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// Toast Notifications
function showToast(message, type = 'success') {
    const toast = document.getElementById('messageToast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Start New Game
async function startNewGame() {
    const playerName = document.getElementById('playerName').value.trim();
    const shopName = document.getElementById('shopName').value.trim();

    if (!playerName || !shopName) {
        showToast('Please enter your name and shop name', 'error');
        return;
    }

    try {
        const response = await fetch('/api/new-game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_name: playerName, shop_name: shopName })
        });

        const data = await response.json();

        if (data.success) {
            currentGameState = data.game_state;
            updateGameDisplay();
            showScreen('gameScreen');
            showToast(data.message);
            document.getElementById('resultsPanel').style.display = 'none';
        } else {
            showToast('Failed to start game', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error starting game', 'error');
    }
}

// Load Saved Game
async function loadGame() {
    try {
        const response = await fetch('/api/load-game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();

        if (data.success) {
            currentGameState = data.game_state;
            updateGameDisplay();
            showScreen('gameScreen');
            showToast(data.message);
        } else {
            showToast(data.error || 'No saved game found', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error loading game', 'error');
    }
}

// Save Game
async function saveGame() {
    try {
        const response = await fetch('/api/save-game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message);
        } else {
            showToast(data.error || 'Failed to save game', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error saving game', 'error');
    }
}

// Play One Day
async function playDay() {
    const cupPrice = parseFloat(document.getElementById('cupPrice').value);
    const coffeeToBuy = parseInt(document.getElementById('coffeeToBuy').value) || 0;
    const advertising = parseFloat(document.getElementById('advertising').value) || 0;

    if (!cupPrice || cupPrice <= 0) {
        showToast('Please enter a valid price', 'error');
        return;
    }

    // Calculate total cost
    const totalCost = coffeeToBuy + advertising;
    if (totalCost > currentGameState.cash) {
        showToast('Not enough cash for these purchases!', 'error');
        return;
    }

    try {
        const response = await fetch('/api/play-day', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                cup_price: cupPrice,
                coffee_to_buy: coffeeToBuy,
                advertising: advertising
            })
        });

        const data = await response.json();

        if (data.success) {
            currentGameState = data.game_state;
            displayDayResults(data.day_result);
            updateGameDisplay();

            // Reset inputs
            document.getElementById('coffeeToBuy').value = 0;
            document.getElementById('advertising').value = 0;

            // Check for game over
            if (data.game_over) {
                setTimeout(() => {
                    showGameOver(data.message);
                }, 2000);
            }
        } else {
            showToast(data.error || 'Error processing day', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error playing day', 'error');
    }
}

// Display Day Results
function displayDayResults(result) {
    const panel = document.getElementById('resultsPanel');
    const content = document.getElementById('resultsContent');

    const profit = result.gross_profit;
    const profitClass = profit > 0 ? 'positive' : profit < 0 ? 'negative' : '';

    let html = `
        <div class="result-item">
            <span class="result-label">🌡️ Temperature:</span>
            <span class="result-value">${result.temperature}°F</span>
        </div>
        <div class="result-item">
            <span class="result-label">☕ Cups Sold:</span>
            <span class="result-value">${result.cups_sold}</span>
        </div>
        <div class="result-item">
            <span class="result-label">💰 Gross Profit:</span>
            <span class="result-value ${profitClass}">$${profit.toFixed(2)}</span>
        </div>
    `;

    if (result.buy_result) {
        const buyClass = result.buy_result.success ? 'positive' : 'negative';
        html += `
            <div class="result-item">
                <span class="result-label">📦 Inventory Purchase:</span>
                <span class="result-value ${buyClass}">${result.buy_result.message}</span>
            </div>
        `;
    }

    content.innerHTML = html;
    panel.style.display = 'block';
}

// Update Game Display
function updateGameDisplay() {
    if (!currentGameState) return;

    document.getElementById('shopNameDisplay').textContent = currentGameState.shop_name;
    document.getElementById('dayDisplay').textContent = currentGameState.day;
    document.getElementById('cashDisplay').textContent = `$${currentGameState.cash.toFixed(2)}`;
    document.getElementById('inventoryDisplay').textContent = `${currentGameState.coffee_inventory} cups`;

    // Temperature will be updated after each day is played
    const tempDisplay = document.getElementById('temperatureDisplay');
    if (!tempDisplay.textContent || tempDisplay.textContent === '-') {
        tempDisplay.textContent = 'Play to see';
    }
}

// Show Game Over
function showGameOver(message) {
    document.getElementById('gameOverMessage').textContent = message;

    const finalStats = `
        <div class="result-item">
            <span class="result-label">Days Survived:</span>
            <span class="result-value">${currentGameState.day - 1}</span>
        </div>
        <div class="result-item">
            <span class="result-label">Total Sales Transactions:</span>
            <span class="result-value">${currentGameState.total_sales}</span>
        </div>
        <div class="result-item">
            <span class="result-label">Final Cash:</span>
            <span class="result-value negative">$${currentGameState.cash.toFixed(2)}</span>
        </div>
    `;

    document.getElementById('finalStats').innerHTML = finalStats;
    showScreen('gameOverScreen');
}

// View Sales History
function viewHistory() {
    if (!currentGameState || !currentGameState.sales_history || currentGameState.sales_history.length === 0) {
        showToast('No sales history yet', 'error');
        return;
    }

    let html = '<table class="history-table"><thead><tr>';
    html += '<th>Day</th><th>Temp (°F)</th><th>Price</th><th>Advertising</th><th>Sold</th>';
    html += '</tr></thead><tbody>';

    currentGameState.sales_history.forEach(sale => {
        html += '<tr>';
        html += `<td>${sale.day}</td>`;
        html += `<td>${sale.temp}°F</td>`;
        html += `<td>$${sale.cup_price.toFixed(2)}</td>`;
        html += `<td>$${sale.advertising.toFixed(2)}</td>`;
        html += `<td>${sale.cups_sold}</td>`;
        html += '</tr>';
    });

    html += '</tbody></table>';

    document.getElementById('historyContent').innerHTML = html;
    document.getElementById('historyModal').classList.add('active');
}

// Close History Modal
function closeHistory() {
    document.getElementById('historyModal').classList.remove('active');
}

// Quit Game
function quitGame() {
    if (confirm('Are you sure you want to quit? Make sure to save your game first!')) {
        location.reload();
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('historyModal');
    if (event.target === modal) {
        closeHistory();
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && document.getElementById('startScreen').classList.contains('active')) {
        startNewGame();
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Coffee Shop Simulator loaded!');
});
