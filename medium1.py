from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import json
import os

app = Flask(__name__)
auth = HTTPBasicAuth()


# Загрузка користувачів з файлу
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)


users = load_users()


# Загрузка товарів з файлу
def load_items():
    if os.path.exists('items.json'):
        with open('items.json', 'r') as f:
            return json.load(f)
    return {}


items = load_items()


# Аутентифікація користувачів
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None


# Ендпоінт для отримання всіх товарів
@app.route('/items', methods=['GET'])
@auth.login_required
def get_items():
    return jsonify(items)


# Ендпоінт для додавання нового товару
@app.route('/items', methods=['POST'])
@auth.login_required
def create_item():
    if not request.json or 'name' not in request.json or 'price' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    item_id = str(len(items) + 1)  # Генерація нового ID
    item = {
        'name': request.json['name'],
        'price': request.json['price']
    }
    items[item_id] = item

    # Запис в items.json
    with open('items.json', 'w') as f:
        json.dump(items, f)

    return jsonify(item), 201


# Ендпоінт для отримання товару за ID
@app.route('/items/<id>', methods=['GET'])
@auth.login_required
def get_item(id):
    if id in items:
        return jsonify(items[id])
    return jsonify({'error': 'Item not found'}), 404


# Ендпоінт для оновлення товару
@app.route('/items/<id>', methods=['PUT'])
@auth.login_required
def update_item(id):
    if id not in items:
        return jsonify({'error': 'Item not found'}), 404

    if not request.json or 'name' not in request.json or 'price' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    item = {
        'name': request.json['name'],
        'price': request.json['price']
    }
    items[id] = item

    # Запис в items.json
    with open('items.json', 'w') as f:
        json.dump(items, f)

    return jsonify(item)


# Ендпоінт для видалення товару
@app.route('/items/<id>', methods=['DELETE'])
@auth.login_required
def delete_item(id):
    if id in items:
        del items[id]

        # Запис в items.json
        with open('items.json', 'w') as f:
            json.dump(items, f)

        return jsonify({'result': True})
    return jsonify({'error': 'Item not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
