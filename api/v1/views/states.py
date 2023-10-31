#!/usr/bin/python3
"""View for State objects default API actions"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


# Route for retrieving all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


# Route for retrieving a specific State object by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


# Route for deleting a specific State object by ID
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# Route for creating a new State object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


# Route for updating an existing State object by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
