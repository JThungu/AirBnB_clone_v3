#!/usr/bin/python3
"""
Create a new view for State objects - handles all default RESTful API actions.
"""

# Import necessary modules
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
states = {}


@app.route('/states', methods=['GET'])
def get_all_states():
    return jsonify(list(states.values()))


@app.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    if state_id in states:
        return jsonify(states[state_id])
    else:
        abort(404)


@app.route('/states', methods=['POST'])
def create_state():
    data = request.get_json()
    if data and 'name' in data:
        new_state = {'id': len(states) + 1, 'name': data['name']}
        states[str(new_state['id'])] = new_state
        return jsonify(new_state), 201
    else:
        abort(400, 'Invalid data or missing name')


@app.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    if state_id in states:
        data = request.get_json()
        if data:
            states[state_id]['name'] = data.get('name', states[state_id]['name'])
            return jsonify(states[state_id]), 200
        else:
            abort(400, 'Invalid data')
    else:
        abort(404)


@app.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    if state_id in states:
        del states[state_id]
        return jsonify({}), 200
    else:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400


if __name__ == '__main__':
    app.run(debug=True)
