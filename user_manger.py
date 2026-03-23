import json
import os

DB_FILE = "users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_users(users_data):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(users_data, file, indent=4)

def register_user(email, password=0, first_name="", last_name="", birth_date="", financial_data=None):
    users = load_users()
    if email in users:
        return False, "User exists"
    users[email] = {
        "password": str(password),
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date,
        "balance": 1000,
        "financial_info": financial_data or {}
    }
    save_users(users)
    return True, "Success"