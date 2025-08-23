from flask import Flask, render_template, request, jsonify
import os
#import plotly.express as px this line is breaking code

# My Script Imports
from selection_validation import validate_selected_icons
from calculations import compute_metrics

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    squaddie_icons = [
    "Barbarian", "Greg", "Colt", "El Primo", "Shelly", "Chicken", "Trader", "Goblin",
    "Mavis", "Heavy", "Poco", "Bo", "Archer", "Nita", "Medic", "Dynamike", "Hog Rider",
    "Penny", "Frank", "Knuckles", "Bandit", "Wizard", "Tank", "Ice Wizard", "Miner",
    "Witch", "Max", "Dr T", "Jessie", "Tails", "Leon", "Battle Healer", "Pam", "Bea",
    "Colonel Ruffs", "Optimus Prime", "Elita-1"]
    
    hero_icons = [
        "Barbarian King", "Archer Queen", "Sonic", "Mortis", "Spike", "Royale King"]
    
    return render_template('index.html', squaddie_icons=squaddie_icons, hero_icons=hero_icons)

@app.route('/process', methods=['POST'])
def process():
    selected = request.form.getlist('selected_icons')
    print("Selected icons:", selected)
    # Run your Python calculations here...
    return f"Received: {', '.join(selected)}"

@app.route('/update_selection', methods=['POST'])
def update_selection():
    data = request.get_json(silent=True) or {}
    selected_icons = data.get('selected_icons', [])
    
    # Validate selections 
    valid_selection = validate_selected_icons(selected_icons)
    
    # Compute metrics
    metrics = compute_metrics(valid_selection)

    # Debug logs
    print("Received selection:", valid_selection)
    print("Metrics:", metrics)


    return jsonify({
        "message": "Selections processed successfully",
    }), 200

@app.route("/chart-data", methods=["POST"])
def chart_data():
    payload = request.get_json(silent=True) or {}
    selected = payload.get("selected_icons", [])

    # Build a time series using your existing logic on each prefix of selections
    xs = []
    squaddie_levels_series = []
    hero_upgrades_total_series = []
    score_series = []

    for i in range(1, len(selected) + 1):
        prefix = selected[:i]
        valid = validate_selected_icons(prefix)
        metrics = compute_metrics(valid)  # your existing totals/score

        xs.append(i)
        squaddie_levels_series.append(metrics["total_squaddie_levels"])
        hero_upgrades_total_series.append(metrics["hero_upgrades_total"])  # powers+traits+turbo
        score_series.append(metrics["score"])

    # Also return the latest snapshot in case you want it for debugging/UI
    latest_valid = validate_selected_icons(selected)
    latest_metrics = compute_metrics(latest_valid)

    return jsonify({
        "x": xs,
        "squaddie_levels": squaddie_levels_series,
        "hero_upgrades_total": hero_upgrades_total_series,
        "score": score_series,
        "latest_metrics": latest_metrics
    }), 200



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
