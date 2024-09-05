import requests
import json
import time
import random
import string


BASE_URL = "http://127.0.0.1:8080"

def create_document(key, document):
    url = f"{BASE_URL}/documents/{key}"
    response = requests.post(url, json=document)
    if response.status_code == 200:
        print("Document created successfully")
    else:
        print(f"Failed to create document: {response.status_code}")

def get_document(key):
    url = f"{BASE_URL}/documents/{key}"
    response = requests.get(url)
    if response.status_code == 200:
        document = response.json()
        print("Document retrieved:", json.dumps(document, indent=2))
    else:
        print(f"Failed to retrieve document: {response.status_code}")

def delete_document(key):
    url = f"{BASE_URL}/documents/{key}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("Document deleted successfully")
    else:
        print(f"Failed to delete document: {response.status_code}")
    
def save_data(filename):
    url = f"{BASE_URL}/save/{filename}"
    response = requests.post(url)
    if response.status_code == 200:
        print("Data saved successfully")
    else:
        print(f"Failed to save data: {response.status_code}")

def load_data(filename):
    url = f"{BASE_URL}/load/{filename}"
    response = requests.post(url)
    if response.status_code == 200:
        print("Data loaded.")
    else:
        print(f"Failed to load data: {response.status_code}")

def generate_random_data():
    return {
        "data": {
            "field1": ''.join(random.choices(string.ascii_letters + string.digits, k=8)),  # случайная строка из 8 символов
            "field2": random.randint(1, 1000),  # случайное число от 1 до 1000
            "field3": random.choice([True, False]),  # случайный выбор между True и False
        }
    }

def benchmark(time_limit):
    start_time = time.time()
    request_count = 0

    # Метрики для замеров времени выполнения
    create_times = []
    get_times = []
    delete_times = []

    while time.time() - start_time < time_limit:
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # случайный ключ для документа
        document = generate_random_data()  # генерируем случайные данные для документа

        # Замер времени на создание документа
        create_start = time.time()
        create_document(key, document)
        create_times.append(time.time() - create_start)

        # Замер времени на получение документа
        get_start = time.time()
        get_document(key)
        get_times.append(time.time() - get_start)

        # Замер времени на удаление документа
        delete_start = time.time()
        delete_document(key)
        delete_times.append(time.time() - delete_start)

        request_count += 3

    elapsed_time = time.time() - start_time

    # Вычисление среднего времени выполнения каждой операции
    avg_create_time = sum(create_times) / len(create_times) if create_times else 0
    avg_get_time = sum(get_times) / len(get_times) if get_times else 0
    avg_delete_time = sum(delete_times) / len(delete_times) if delete_times else 0

    print(f"Benchmark finished. Total requests made: {request_count} in {elapsed_time:.2f} seconds.")
    print(f"Average times (seconds) - Create: {avg_create_time:.6f}, Get: {avg_get_time:.6f}, Delete: {avg_delete_time:.6f}")
    save_data("benchmark_data")
benchmark(1)