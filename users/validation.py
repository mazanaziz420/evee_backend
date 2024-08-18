from flask import jsonify
import re
from jsonschema import validate, ValidationError

# JSON Schema definitions for input validation
SIGNUP_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string", "minLength": 8},  # Updated to match the minimum length required by password validation
        "user_type": {"type": "string"}
    },
    "required": ["username", "email", "password"]
}

LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string", "minLength": 8}  # Updated to match the minimum length required by password validation
    },
    "required": ["email", "password"]
}

ONLY_EMAIL_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"}
    },
    "required": ["email"]
}

# Password validation function
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

# Validation function for signup input
def validate_signup_input(request_json):
    try:
        validate(request_json, SIGNUP_SCHEMA)
        password = request_json.get("password")
        is_valid, error_message = validate_password(password)
        if not is_valid:
            return {"error": error_message, "status": False}
        return {"error": None, "status": True}
    except ValidationError as e:
        return {"error": str(e.message), "status": False}

# Validation function for login input
def validate_login_input(request_json):
    try:
        validate(request_json, LOGIN_SCHEMA)
        password = request_json.get("password")
        is_valid, error_message = validate_password(password)
        if not is_valid:
            return {"error": error_message, "status": False}
        return {"error": None, "status": True}
    except ValidationError as e:
        return {"error": str(e.message), "status": False}

# Validation function for email-only input (e.g., forgot password)
def validate_only_email_input(request_json):
    try:
        validate(request_json, ONLY_EMAIL_SCHEMA)
        return {"error": None, "status": True}
    except ValidationError as e:
        return {"error": str(e.message), "status": False}
