# calculations.py
"""
Calculation utilities for totals and score.
Kept identical to your current behavior, plus extra totals.
"""

from typing import List, Dict, Any

def compute_metrics(valid_selection: List[Dict[str, Any]]) -> Dict[str, int]:
    total_squaddie_levels = sum(i['level'] for i in valid_selection if i['panel'] == 'squaddies') # this variable will be the new dps
    hero_count            = sum(1 for i in valid_selection if i['panel'] == 'heroes')             # this variable will be the new total health 

    total_hero_powers = sum(i['powers'] for i in valid_selection if i['panel'] == 'heroes')
    total_hero_traits = sum(i['traits'] for i in valid_selection if i['panel'] == 'heroes')
    total_hero_turbo  = sum(i['turbo']  for i in valid_selection if i['panel'] == 'heroes')
    hero_upgrades_total = total_hero_powers + total_hero_traits + total_hero_turbo

    # Keep your current score formula unchanged
    score = total_squaddie_levels * 10 + hero_count * 50

    return {
        "total_squaddie_levels": total_squaddie_levels,
        "hero_count": hero_count,
        "total_hero_powers": total_hero_powers,
        "total_hero_traits": total_hero_traits,
        "total_hero_turbo": total_hero_turbo,
        "hero_upgrades_total": hero_upgrades_total,
        "score": score,
    }
