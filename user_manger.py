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


def register_user(email, password, first_name="", last_name="", birth_date=""):
    users = load_users()
    if email in users:
        return False, "המשתמש כבר קיים במערכת."

    # במערכת אמיתית נצפין את הסיסמה, אך לצורך הסימולציה נשמור כטקסט
    users[email] = {
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date,
        "balance": 1000  # סכום התחלתי לסימולציה
    }
    save_users(users)
    return True, "ההרשמה בוצעה בהצלחה!"


def login_user(email, password):
    users = load_users()
    if email not in users:
        return False, "אימייל לא נמצא."
    if users[email]["password"] != password:
        return False, "סיסמה שגויה."
    return True, "התחברת בהצלחה!"