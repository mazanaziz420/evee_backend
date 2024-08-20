from flask import Blueprint, request, jsonify
from services.auth_service import authenticate_user, generate_access_token
from services.email_service import send_verification_email
from services.verification_service import generate_verification_code
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models import *

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    existing_user = User.find_by_email(data['email'])
    
    if existing_user:
        return jsonify({"message": "User already exists"}), 400
    
    verification_code = generate_verification_code()

    user = User(
        email=data['email'],
        password=data['password'],
        full_name=data['full_name'],
        username=data['username'],
        user_type=data['user_type'],
        verification_code=verification_code
    )
    
    user.save()
    send_verification_email(data['email'], verification_code)

    # Return user information except for the password
    user_info = {
        "email": user.email,
        "full_name": user.full_name,
        "username": user.username,
        "user_type": user.user_type,
        "is_verified": user.is_verified
    }
    
    return jsonify({
        "message": "User created. Verification email sent.",
        "user": user_info
    }), 201

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.find_by_email(data['email'])
    
    if not user or not User.verify_password(user['password'], data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    if not user['is_verified']:
        return jsonify({"message": "Email not verified"}), 403

    token = generate_access_token(user['email'])

    user_info = {
        "email": user['email'],
        "full_name": user['full_name'],
        "username": user['username'],
        "user_type": user['user_type'],
        "is_verified": user['is_verified']
    }

    return jsonify({
        "token": token,
        "user": user_info
    }), 200

@users_bp.route('/get_vcode', methods=['POST'])
def get_verification_code():
    data = request.json
    user = User.find_by_email(data['email'])
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    verification_code = generate_verification_code()
    mongo.db['User'].update_one(
            {"email": data['email']},
            {"$set": {"verification_code": verification_code}}
        )
    send_verification_email(data['email'], verification_code, is_signup=False)

    return jsonify({"message": "Verification code sent"}), 200

@users_bp.route('/reset_password/verify', methods=['POST'])
def verify_code():
    data = request.json
    verification_code = data.get('verification_code')
    
    if not verification_code:
        return jsonify({"message": "Invalid verification code"}), 400
    
    user = User.find_by_email(data['email'])
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user['verification_code'] == verification_code:
        mongo.db['User'].update_one(
            {"email": data['email']},
            {"$set": {"is_verified": True}}
        )
        return jsonify({"message": "Verification successful"}), 200
    
    return jsonify({"message": "Invalid verification code"}), 400


@users_bp.route('/reset_password/update', methods=['POST'])
def reset_password():
    data = request.json
    user = User.find_by_email(data['email'])
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user['is_verified'] == True:
        new_password_hash = generate_password_hash(data['password'])
        mongo.db['User'].update_one(
            {"email": data['email']},
            {"$set": {"password": new_password_hash}}
        )
        return jsonify({"message": "Password updated successfully"}), 200
    
    return jsonify({"message": "Invalid verification code"}), 400
