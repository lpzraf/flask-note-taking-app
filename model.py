import json

def load_db():
    with open("notes_data_db.json") as f:
        return json.load(f)

def save_db():
    with open("notes_data_db.json", 'w') as f:
        return json.dump(db, f)

db = load_db()