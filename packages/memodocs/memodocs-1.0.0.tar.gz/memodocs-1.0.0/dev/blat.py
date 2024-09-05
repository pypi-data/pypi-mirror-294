import memodocs
import json

# Создание нового документа с различными типами данных
data = {
    "string_key": "string_value",
    "int_key": 42,
    "float_key": 3.14,
    "array_key": [1, 2, 3],
    "object_key": {"nested_key": "nested_value"}
}
data_dict = {k: v for k, v in data.items()}
doc = memodocs.PyDocument(data_dict)

# Создание нового экземпляра базы данных
db = memodocs.PyDatabase()

# Вставка документа в базу данных
db.insert("document1", doc)

# Получение документа из базы данных
retrieved_doc = db.get("document1")
if retrieved_doc:
    # Преобразование данных обратно в Python-тип
    data = retrieved_doc.get_data()
    print("Retrieved document data:", json.dumps(data, indent=2))
else:
    print("Document not found")

# Удаление документа из базы данных
deleted_doc = db.delete("document1")
if deleted_doc:
    data = deleted_doc.get_data()
    print("Deleted document data:", json.dumps(data, indent=2))
else:
    print("Document not found for deletion")

# Сохранение базы данных в файл
db.save_to_file("database.json")

# Загрузка базы данных из файла
db.load_from_file("database.json")
