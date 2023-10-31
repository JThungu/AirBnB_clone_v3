#!/usr/bin/python3
""" View for State objects default API actions """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """ Retrieves the list of all State objects """
    d_states = storage.all(State)
    return jsonify([obj.to_dict() for obj in d_states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def r_state_id(state_id=None):
    """ Retrieves a State object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id=None):
    """ Deletes a State object """
    state = storage.get("State", state_id)
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State object """
    new_state = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """ Updates a State object """
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()
