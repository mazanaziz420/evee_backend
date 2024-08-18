import os
from dotenv import load_dotenv
import jwt
from datetime import datetime
import secrets
import string

def generate_verification_code():
    code = ''.join(secrets.choice(string.digits) for _ in range(6))
    return int(code)

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")

def generate_jwt_token(content):
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    now = datetime.now()
    token = "e"+str(now.strftime("%S%M%H"))+str(encoded_content)+"_!-@_#-$_%-^_&-*_(-)"+str(now.strftime("%d%m%Y%H%M%S"))
    return token
