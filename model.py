import json

# notes db
def load_db():
    with open("notes_data_db.json") as f:
        return json.load(f)

def save_db():
    with open("notes_data_db.json", 'w') as f:
        return json.dump(db, f)

# user db
def load_user_db():
    with open("users_data_db.json") as f:
        return json.load(f)

def save_user_db():
    with open("users_data_db.json", 'w') as f:
        return json.dump(user_db, f)


db = load_db()
user_db = load_user_db()