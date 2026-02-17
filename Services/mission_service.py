# from .pilot_service import get_pilots
# from .pilot_service import is_available_today
# from .drone_service import get_drones
# from dateutil import parser
# from datetime import date

# def find_best_match(requirement):
#     pilots, _ = get_pilots()
#     drones, _ = get_drones()
#     location = requirement.get('location', '').lower()
#     skill = requirement.get('skill', '').lower()
#     capability = requirement.get('capability', '').lower()
    
#     # Score pilots
#     pilot_scores = []
#     for p in pilots:
#         if not is_available_today(p):
#             continue
#         score, reasons = 0, []
#         if location and location in p.get('location', '').lower():
#             score += 30; reasons.append(f"Located in {p['location']}")
#         if skill and skill in p.get('skills', '').lower():
#             score += 40; reasons.append(f"Has {skill} skills")
#         certs = p.get('certifications', '').lower()
#         if 'advanced' in certs or 'master' in certs:
#             score += 20; reasons.append("Advanced certification")
#         if p.get('status') == 'Available':
#             score += 10; reasons.append("Immediately available")
#         if score > 0:
#             pilot_scores.append({'pilot': p, 'score': score, 'reasons': reasons})
    
#     # Score drones
#     drone_scores = []
#     for d in drones:
#         if d.get('status') != 'Available':
#             continue
#         score, reasons = 0, []
#         if location and location in d.get('location', '').lower():
#             score += 30; reasons.append(f"Located in {d['location']}")
#         if capability and capability in d.get('capabilities', '').lower():
#             score += 40; reasons.append(f"Has {capability} capability")
#         due_str = str(d.get('maintenance_due', '')).strip()
#         if due_str:
#             try:
#                 due = parser.parse(due_str).date()
#                 days_until = (due - date.today()).days
#                 if days_until > 30: score += 20; reasons.append("Maintenance OK (>30 days)")
#                 elif days_until > 7: score += 10; reasons.append(f"Maintenance in {days_until} days")
#             except: pass
#         if score > 0:
#             drone_scores.append({'drone': d, 'score': score, 'reasons': reasons})
    
#     pilot_scores.sort(key=lambda x: x['score'], reverse=True)
#     drone_scores.sort(key=lambda x: x['score'], reverse=True)
    
#     best_combo = {'pilot': pilot_scores[0], 'drone': drone_scores[0]} if pilot_scores and drone_scores else None
    
#     return {'top_pilots': pilot_scores[:3], 'top_drones': drone_scores[:3], 'best_combo': best_combo}
