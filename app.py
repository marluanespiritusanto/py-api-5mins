from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from os import environ

app = Flask(__name__)
app.config["MONGO_URI"] = environ.get("MONGO_URI")
mongo = PyMongo(app)
db = mongo.db


@app.route('/api/todo')
def getTodos():
    _todos = db.todo.find()
    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'todo': todo['todo']
        }
        data.append(item)

    return jsonify(status=True, data=data)


@app.route('/todo', methods=['POST'])
def createTodo():
    data = request.get_json(force=True)
    item = {
        'todo': data['todo']
    }
    db.todo.insert_one(item)

    return jsonify(status=True, message='To-do saved successfully!'), 201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
