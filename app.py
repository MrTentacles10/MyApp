from flask import Flask, render_template, request, jsonify
import os

# My Script Imports
from selection_validation import validate_selected_icons
from calculations import compute_metrics
import plotly.express as px

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

    # Example: compute something from selections
    # (Replace with your real logic)
    # We'll produce two series:
    #   - squaddie_levels: cumulative level per selection order
    #   - hero_upgrades: sum(powers+traits+turbo) per hero selection
    x = []
    squaddie_levels = []
    hero_upgrades = []

    cum_sq = 0
    for idx, item in enumerate(selected, start=1):
        x.append(idx)
        if item.get("panel") == "squaddies" and isinstance(item.get("level"), int):
            cum_sq += item["level"]
        squaddie_levels.append(cum_sq)

        if item.get("panel") == "heroes":
            p = item.get("powers") or 0
            t = item.get("traits") or 0
            u = item.get("turbo")  or 0
            hero_upgrades.append(p + t + u)
        else:
            hero_upgrades.append(0)

    return jsonify({
        "x": x,
        "squaddie_levels": squaddie_levels,
        "hero_upgrades": hero_upgrades
    })



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
