from flask import Flask, render_template, request
import os

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
    data = request.get_json()
    selected_icons = data.get('selected_icons', [])

    # Ensure each entry has name and level
    valid_selection = []
    for icon in selected_icons:
        name = icon.get('name')
        level = icon.get('level')
        panel = icon.get('panel')

        # Validate: level must be int between 1 and 5
        if not isinstance(level, int) or level < 1 or level > 5:
            continue  # Skip invalid entries

        valid_selection.append({
            'name': name,
            'level': level,
            'panel': panel
        })

    # You can now use `valid_selection` in your backend logic
    print("Received selection:", valid_selection)

    return '', 204


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
