from memodocs import PyDatabase, PyDocument

# Создание экземпляра базы данных
db = PyDatabase()

# Создание документа
doc1 = PyDocument({
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
})

# Добавление документа в базу данных
db.insert("user1", doc1)

# Получение документа по ключу
retrieved_doc = db.get("user1")

# Вывод данных документа
print("Retrieved document data:", retrieved_doc)