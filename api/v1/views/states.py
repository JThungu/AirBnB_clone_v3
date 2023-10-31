#!/usr/bin/python3
""" View for State objects default API actions """
from flask import Blueprint, jsonify, request, abort
from models import State  # Import your State model

states_bp = Blueprint('states', __name__)

# Retrieve all State objects
@states_bp.route('/api/v1/states', methods=['GET'])
def get_all_states():
    states = State.query.all()
    return jsonify([state.to_dict() for state in states])

# Retrieve a specific State object
@states_bp.route('/api/v1/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

# Delete a State object
@states_bp.route('/api/v1/states/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    # Delete the state
    # Your deletion logic here
    return jsonify({}), 200

# Create a new State
@states_bp.route('/api/v1/states', methods=['POST'])
def create_state():
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    # Create a new State using the data
    # Your creation logic here
    new_state = State(name=data['name'])
    # Save the state
    # Your save logic here
    return jsonify(new_state.to_dict()), 201

# Update a State object
@states_bp.route('/api/v1/states/<int:state_id>', methods=['PUT'])
def update_state(state_id):
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    
    # Update state attributes
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    # Save the updated state
    # Your save logic here
    return jsonify(state.to_dict()), 200

# Your other helper functions or imports can go here

