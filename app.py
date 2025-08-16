from flask import Flask, render_template, request, jsonify
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
    data = request.get_json(silent=True) or {}
    selected_icons = data.get('selected_icons', [])

    valid_selection = []
    for icon in selected_icons:
        name  = icon.get('name')
        panel = icon.get('panel')
        if not name or not panel:
            continue

        if panel == 'squaddies':
            level = icon.get('level')
            if isinstance(level, int) and 1 <= level <= 5:
                valid_selection.append({'name': name, 'panel': panel, 'level': level})
            # else: skip bad squaddie entries
        elif panel == 'heroes':
            # Your current UI doesn't send hero levels yet—accept as-is
            valid_selection.append({'name': name, 'panel': panel})

    # ----- do calculations AFTER the loop -----
    total_squaddie_levels = sum(i['level'] for i in valid_selection if i['panel'] == 'squaddies')
    hero_count = sum(1 for i in valid_selection if i['panel'] == 'heroes')
    score = total_squaddie_levels * 10 + hero_count * 50  # example score

    print("Received selection:", valid_selection)
    print("Total squaddie levels:", total_squaddie_levels)
    print("Hero count:", hero_count)
    print("Score:", score)

    # Return JSON (your frontend calls response.json())
    return jsonify({
        "message": "Selections processed successfully",
        "total_squaddie_levels": total_squaddie_levels,
        "hero_count": hero_count,
        "score": score
    }), 200



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
