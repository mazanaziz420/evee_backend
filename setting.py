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

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLPORT = int(os.getenv("MYSQLPORT"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")

def generate_jwt_token(content):
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    now = datetime.now()
    token = "e"+str(now.strftime("%S%M%H"))+str(encoded_content)+"_!-@_#-$_%-^_&-*_(-)"+str(now.strftime("%d%m%Y%H%M%S"))
    return token

