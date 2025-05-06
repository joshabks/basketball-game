from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)
user_points = 100

# Get the games for a specific date
def get_games(date):
    # Log the date being passed to check the format
    print(f"Fetching games for date: {date}")
    
    try:
        datetime.strptime(date, '%Y-%m-%d')  # Verify correct format
    except ValueError:
        print(f"Invalid date format: {date}")
        return []  # If the date is invalid, return an empty list

    # Make API call to fetch games for the date
    url = f"https://www.balldontlie.io/api/v1/games?start_date={date}&end_date={date}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any API errors
        data = response.json().get("data", [])
        
        # Log the API response to see what data we are getting
        print(f"API response for {date}: {data}")
        
        if not data:
            print(f"No games found for {date}")
        
        return data
    except Exception as e:
        print(f"Error fetching games for {date}: {e}")
        return []

@app.route("/")
def index():
    today = datetime.today().strftime('%Y-%m-%d')
    games = get_games(today)
    return render_template("index.html", games=games, points=user_points, today=today)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    global user_points

    if request.method == "POST":
        player = request.form["player"]
        prediction = int(request.form["prediction"])
        wager = int(request.form["wager"])
        game_id = request.form["game_id"]
        prediction_type = request.form["prediction_type"]
        game_date = request.form["game_date"]

        if wager > user_points or wager <= 0:
            return "Invalid wager"

        actual = get_player_stat(player, game_id)

        if
