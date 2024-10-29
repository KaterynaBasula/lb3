from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Зберігання користувачів та товарів
users = {
    "admin": "password"
}

items = {
    1: {"name": "Item 1", "price": 10.0},
    2: {"name": "Item 2", "price": 20.0},
    3: {"name": "Item 3", "price": 30.0}
}

# Аутентифікація
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Отримання всіх товарів
@app.route('/items', methods=['GET'])
@auth.login_required
def get_items():
    return jsonify(items)

# Отримання товару за id
@app.route('/items/<int:item_id>', methods=['GET'])
@auth.login_required
def get_item(item_id):
    item = items.get(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)

# Додавання нового товару
@app.route('/items', methods=['POST'])
@auth.login_required
def create_item():
    if not request.json or 'name' not in request.json or 'price' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    item_id = max(items.keys()) + 1
    item = {
        'name': request.json['name'],
        'price': request.json['price']
    }
    items[item_id] = item
    return jsonify(item), 201

# Оновлення товару
@app.route('/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(item_id):
    item = items.get(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    if not request.json:
        return jsonify({'error': 'Bad request'}), 400

    item['name'] = request.json.get('name', item['name'])
    item['price'] = request.json.get('price', item['price'])
    return jsonify(item)

# Видалення товару
@app.route('/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(item_id):
    item = items.pop(item_id, None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)

