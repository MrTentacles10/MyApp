# selection_validation.py
"""
Validation utilities for incoming selections.
Keeps exactly the same rules you have now.
"""

from typing import List, Dict, Any

def validate_selected_icons(selected_icons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return only valid selections according to current rules."""
    valid_selection = []
    for icon in selected_icons:
        name  = icon.get('name')
        panel = icon.get('panel')
        if not name or not panel:
            continue
        # else: ignore if not name or panel... for now

        if panel == 'squaddies':
            level = icon.get('level')
            if isinstance(level, int) and 1 <= level <= 5:
                valid_selection.append({'name': name, 'panel': panel, 'level': level})

        elif panel == 'heroes':
            powers = icon.get('powers')
            traits = icon.get('traits')
            turbo  = icon.get('turbo')
            if (isinstance(powers, int) and 1 <= powers <= 5 and
                isinstance(traits, int) and 1 <= traits <= 5 and
                isinstance(turbo,  int) and 1 <= turbo  <= 3):
                valid_selection.append({
                    'name': name,
                    'panel': panel,
                    'powers': powers,
                    'traits': traits,
                    'turbo': turbo
                })
        # else: ignore unknown panel

    return valid_selection
