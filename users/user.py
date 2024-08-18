from flask import request, Blueprint, jsonify, session
from .send_email import send_verification_email
from datetime import datetime
from .query import *
from commons.setting import generate_verification_code, generate_jwt_token
from commons.utils import HttpCodes
from commons.decorator import protected
from .validation import *
from users.models import UserType

user_bp = Blueprint("user", __name__)


def send_verification_code_email(email, username, password, full_name):
    try:
        verification_code = generate_verification_code()
        session['verification_code'] = verification_code
        if username and password and full_name:
            session['username'] = username
            session['password'] = password
            session['full_name'] = full_name

        send_verification_email(email, verification_code)

        return jsonify({"result": "success", "message": "Verification code sent"}), HttpCodes.HTTP_200_OK

    except Exception as e:
        print(e)
        return jsonify({"error": HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR}), HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR


@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        request_json = request.get_json()

        validation_result = validate_signup_input(request_json)
        if not validation_result["status"]:
            return jsonify({"error": validation_result["error"]}), HttpCodes.HTTP_400_BAD_REQUEST

        username = request_json.get('username')
        email = request_json.get('email')
        password = request_json.get('password')
        full_name = request_json.get('full_name')
        user_type_str = request_json.get('user_type')
        verification_code = generate_verification_code()
        
        # Convert user_type_str to UserType enum
        try:
            user_type = UserType[user_type_str]
        except KeyError:
            return jsonify({"error": "Invalid user_type value"}), HttpCodes.HTTP_400_BAD_REQUEST

        query = Users.select().where((Users.email == email) | (Users.username == username))
        if query.exists():
            return jsonify({"error": "Username or email already exists"}), HttpCodes.HTTP_400_BAD_REQUEST
        send_verification_email(email, verification_code)
        password_hash = hash_password(password)
        Users.create(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            verification_code=verification_code,
            user_type=user_type
        )
        user_data = get_login_records(email, password)

        return {"result": "success", "data": user_data}, HttpCodes.HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e), "status": HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR}), HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR
    
@user_bp.route('/get_vcode', methods=['POST'])
def forgot_password():
    try:
        request_json = request.get_json()
        print(request_json)

        validation_result = validate_only_email_input(request_json)
        if not validation_result["status"]:
            return jsonify({"error": validation_result["error"]}), HttpCodes.HTTP_400_BAD_REQUEST

        email = request_json.get('email')
        
        v_code = generate_verification_code()
        print(v_code, email)
        query = Users.update(verification_code=v_code).where(Users.email == email)
        result = query.execute()  # Execute the query and store the result
        if result > 0:  # If rows were affected, result will be greater than 0
            send_verification_email(email, v_code, is_signup=False)
            return jsonify({"result": "success", "message": "Verification code sent"}), HttpCodes.HTTP_200_OK
        else:
            return jsonify({"error": "Invalid email"}), HttpCodes.HTTP_400_BAD_REQUEST

    except Exception as e:
        print(e)
        return jsonify({"error": HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR}), HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR


@user_bp.route('/reset_password/verify', methods=['POST'])
def verify_reset_code():
    try:
        request_json = request.get_json()
        email = request_json.get('email')
        verification_code = request_json.get('verification_code')

        stored_code = list(Users.select(Users.verification_code).where(Users.email == email).dicts())
        stored_code = stored_code[0].get('verification_code')
        if stored_code == verification_code:
            Users.update(verification_code='').where(Users.email == email).execute()
            return jsonify({"result": "success", "message": "Verification code verified"}), HttpCodes.HTTP_200_OK
        else:
            return jsonify({"error": "Invalid verification code"}), HttpCodes.HTTP_400_BAD_REQUEST

    except Exception as e:
        print(e)
        return jsonify({"error": HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR}), HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR


@user_bp.route('/reset_password/update', methods=['POST'])
def save_reset_password():
    try:
        request_json = request.get_json()
        email = request_json.get('email')
        password = request_json.get('password')

        validation_result = validate_login_input(request_json)
        if not validation_result["status"]:
            return jsonify({"error": validation_result["error"]}), HttpCodes.HTTP_400_BAD_REQUEST

        password_hash = hash_password(password)
        update_password(email, password_hash)

        return jsonify({"result": "success", "message": "Password updated"}), HttpCodes.HTTP_200_OK

    except Exception as e:
        print(e)
        return jsonify({"error": HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR}), HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR


@user_bp.route('/verify_signup', methods=['POST'])
def verify_email():
    try:
        request_json = request.get_json()
        email = request_json.get('email')
        password = request_json.get('password')
        submitted_code = request_json.get('verification_code')
        records = get_login_records(email, password)
        if records:
            stored_code = Users.select(Users.verification_code).where(Users.email == email).dicts()
            stored_code = list(stored_code)
            if stored_code[0]['verification_code'] == submitted_code:
                now = datetime.now()
                jwt_token = generate_jwt_token({"user": str(now.strftime("%S%M%H"))})
                Users.update(verification_code='').where(Users.email == email).execute()
                update_user_token(records, jwt_token)
                return jsonify({"result": "success", "data": records, "token": jwt_token}), HttpCodes.HTTP_200_OK
            else:
                return jsonify({"error": "Invalid verification code"}), HttpCodes.HTTP_400_BAD_REQUEST

    except Exception as e:
        print(e)
        return jsonify({"error": HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR}), HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR


@user_bp.route('/login', methods=['POST'])
def login():
    try:
        request_json = request.get_json()
        email = request_json.get('email')
        password = request_json.get('password')
        records = get_login_records(email, password)
        validation_result = validate_login_input(request_json)
        if not validation_result["status"]:
            return jsonify({"error": validation_result["error"]}), HttpCodes.HTTP_400_BAD_REQUEST
        if records:
            now = datetime.now()
            jwt_token = generate_jwt_token({"user": str(now.strftime("%S%M%H"))})
            update_user_token(records, jwt_token)
            return jsonify({"result": 1, "data": records, "token": jwt_token}), HttpCodes.HTTP_200_OK
        else:
            return jsonify(
                {"error": "Invalid login credentials"}), HttpCodes.HTTP_401_UNAUTHORIZED

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR


@user_bp.route('/logout', methods=['POST'])
@protected
def logout(id):
    id = id[0]["id"]

    result = remove_token_for_logout(id)
    if result:
        return jsonify({"result": "success"}), HttpCodes.HTTP_200_OK
    else:
        return jsonify({"error": HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR}), HttpCodes.HTTP_500_INTERNAL_SERVER_ERROR
