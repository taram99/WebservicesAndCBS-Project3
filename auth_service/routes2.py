from jwtauth import validating_jwt, generating_jwt
from flask import Blueprint, jsonify, request

#Creates blueprint for authentication routes and allows auth service to be registered in app2.py
auth_routes = Blueprint("auth_routes", __name__)
#In memory storage for users
users = {}

@auth_routes.route("/users", methods=["POST"])
def create_user():
    """
    Registers new user. 
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    #Prevents duplicate users
    if username in users:
        return "Duplicate", 409
    #Stores user credentials in memory
    users[username] = password
    return "", 201
    

@auth_routes.route("/users", methods=["PUT"])
def update_password():
    """
    Updates existing user's password.
    """
    data = request.get_json()
    username = data.get("username")
    password_old = data.get("old-password")
    password_new = data.get("new-password")
    #Verify user exists and old password matches
    if username not in users or users[username] != password_old:
        return "forbidden", 403
    #Updates password
    users[username] = password_new
    return "", 200

@auth_routes.route("/users/login", methods=["POST"])
def login():
    """
    Authenticates user and generates a JWT.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    #Validate credentials
    if username not in users or users[username] != password:
        return "forbidden", 403
    #Generate signed JWT for authenticated user
    token = generating_jwt(username)
    return jsonify({"token": token}), 200

@auth_routes.route("/validate", methods=["POST"])
def validate():
    """
    Validates JWT sent by another service. This endpoint is used by URL shortening service
    to verify authenticated users.
    """
    data = request.get_json()
    token = data.get("token")

    print("Received JSON:", data)

    if not token:
        return "Forbidden", 403
    #Validate token using JWT utility
    username = validating_jwt(token)

    if not username:
        return "Forbidden", 403
    
    return jsonify({"username": username}), 200

