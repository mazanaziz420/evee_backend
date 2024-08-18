from .models import Users
from peewee import JOIN
import hashlib


def get_user_by_email(email):
    return Users.get_or_none(Users.email == email)

def get_user_by_id(user_id):
    return Users.get_or_none(Users.id == user_id)

def hash_password(password):
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def create_user(username, email, password_hash, full_name, user_type):
    return Users.create(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        user_type=user_type
    )

def get_login_records(email, password):
    encrypt_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
    query = Users.select(
        Users.id,
        Users.username,
        Users.full_name,
        Users.email,
        Users.user_type
    ).where(
        Users.email == email,
        Users.password_hash == encrypt_pass
    ).dicts()

    results = list(query)

    user_data = {}

    for result in results:
        user_id = result['id']

        if user_id not in user_data:
            user_data[user_id] = {
                'id': user_id,
                'username': result['username'],
                'full_name': result['full_name'],
                'email': result['email'],
                'user_type': result['user_type'].name
            }

    return list(user_data.values())

def update_password(email, password_hash):
    query = Users.update(password_hash=password_hash).where(Users.email == email)
    query.execute()
    return True

def update_user_token(records, token):
    try:
        Users.update(token=token).where(Users.id == records[0].get("id")).execute()
    except Exception as e:
        print(e)

def remove_token_for_logout(id):
    try:
        Users.update(token=None).where(Users.id == id).execute()
        return True
    except Exception as e:
        print(e)
        return False
