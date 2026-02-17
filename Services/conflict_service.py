from .pilot_service import get_pilots
from .pilot_service import is_available_today
from .drone_service import get_drones
from dateutil import parser
from datetime import date

def analyze_conflicts():
    pilots, _ = get_pilots()
    drones, _ = get_drones()
    conflicts = {'critical': [], 'warning': [], 'info': []}

    # Double-booking pilots
    pilot_assignments = {}
    for p in pilots:
        assign = str(p.get('current_assignment', '')).strip()
        if assign:
            if assign in pilot_assignments:
                conflicts['critical'].append({'type': 'PILOT_DOUBLE_BOOKING', 'message': f"Both {pilot_assignments[assign]['name']} and {p['name']} assigned to '{assign}'"})
            else:
                pilot_assignments[assign] = p

    # Double-booking drones
    drone_assignments = {}
    for d in drones:
        assign = str(d.get('current_assignment', '')).strip()
        if assign:
            if assign in drone_assignments:
                conflicts['critical'].append({'type': 'DRONE_DOUBLE_BOOKING', 'message': f"Multiple drones assigned to '{assign}'"})
            else:
                drone_assignments[assign] = d

    return conflicts
