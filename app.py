from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from Services import pilot_service, drone_service, mission_service, conflict_service

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    pilots, _ = pilot_service.get_pilots()
    drones, _ = drone_service.get_drones()
    return jsonify({
        'status': 'healthy',
        'pilots': len(pilots),
        'drones': len(drones)
    })

@app.route('/api/match', methods=['POST'])
def match():
    data = request.get_json()
    result = mission_service.find_best_match(data)
    return jsonify(result)

@app.route('/api/conflicts')
def conflicts():
    result = conflict_service.analyze_conflicts()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
