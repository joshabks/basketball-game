from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)
user_points = 100

def get_today_games():
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"https://www.balldontlie.io/api/v1/games?start_date={today}&end_date={today}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print("Error getting games:", e)
        return []

def get_player_id(player_name):
    try:
        response = requests.get(f"https://www.balldontlie.io/api/v1/players?search={player_name}")
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[0]["id"] if data else None
    except Exception as e:
        print("Error getting player ID:", e)
        return None

def get_player_stat(player_name, game_id):
    try:
        player_id = get_player_id(player_name)
        if not player_id:
            return None

        stats_url = f"https://www.balldontlie.io/api/v1/stats?game_ids[]={game_id}&player_ids[]={player_id}"
        stats_resp = requests.get(stats_url)
        stats_resp.raise_for_status()
        stats = stats_resp.json().get("data", [])
        if not stats:
            return None

        return stats
