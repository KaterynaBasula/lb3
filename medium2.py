import requests
from requests.auth import HTTPBasicAuth

# Конфігурація
BASE_URL = 'http://127.0.0.1:5000/items'
USERNAME = 'admin'
PASSWORD = 'password'

# Функція для отримання всіх товарів
def get_items():
    response = requests.get(BASE_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Функція для додавання нового товару
def add_item(name, price):
    response = requests.post(BASE_URL, json={'name': name, 'price': price}, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Функція для оновлення товару
def update_item(item_id, name, price):
    response = requests.put(f'{BASE_URL}/{item_id}', json={'name': name, 'price': price}, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Функція для видалення товару
def delete_item(item_id):
    response = requests.delete(f'{BASE_URL}/{item_id}', auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Приклади використання
if __name__ == "__main__":
    print("Отримання товарів:")
    get_items()  # Отримання товарів

    print("\nДодавання нового товару:")
    add_item("Товар 1", 100)  # Додавання товару

    print("\nОтримання товарів після додавання:")
    get_items()  # Отримання товарів

    print("\nОновлення товару:")
    update_item("1", "Оновлений Товар 1", 150)  # Оновлення товару

    print("\nОтримання товарів після оновлення:")
    get_items()  # Отримання товарів

    print("\nВидалення товару:")
    delete_item("1")  # Видалення товару

    print("\nОтримання товарів після видалення:")
    get_items()  # Отримання товарів
