#!/usr/bin/env python3
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()

@app.route('/states', strict_slashes=False)
def states():
    """Displays a HTML page with a list of all State objects"""
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)

@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Displays a HTML page with the cities of a specific State"""
    state = storage.get(State, id)
    if state is None:
        return render_template('9-not_found.html')
    return render_template('9-state.html', state=state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

