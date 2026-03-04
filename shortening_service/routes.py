from flask import request, jsonify, redirect
from utils import is_valid_url, create_short_id
import json
import requests
from database2 import (
does_url_exist, delete_url, update_url_in_db, increment_clicks, url_row, ids_user,
insert_new_url, get_id_by_url, init_db)

def register_routes(app):
    #Registers all URL shortening routes
    #Service depends on authentication service for user validation.

    def retrieve_username_from_token():
        #Extracts JWT token from authentication header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None
        
        try:
            token = auth_header

        except Exception:
            return None
        
        try:
            #Calls authentication service to validate token
            response = requests.post(
                "http://127.0.0.1:8001/validate",
                json={"token": token}
            )

            print("Validate status:", response.status_code)
            print("Validate response:", response.text)  

        except Exception:
            return None
        #Token invalid if not response code 200
        if response.status_code != 200:
            return None
        
        return response.json().get("username")



    def bad_request(msg = "error"):
        """
        Helper function to return standardized 400 responses
        """
        return jsonify({"error": msg}), 400
    
    @app.route("/", methods=["POST"])
    def create_url():
        """
        Creates new short url for given url. Requires authentication.
        """
        data = request.get_json(silent=True)

        #Require authentication
        username = retrieve_username_from_token()
        if not username:
            return "", 403

        #Ensure body is valid json
        if not isinstance(data, dict):
            return bad_request()
        
        url = data.get("url") or data.get("value")

        #Check if url is valid
        if not url or not is_valid_url(url):
            return bad_request()
        
        #Check if url already exists, 201 return to satisfy unit tests
        id_exist = does_url_exist(url)
        if id_exist:
            return jsonify({"warning": "url already exists",
                               "id": id_exist}), 201
            
        short_id = create_short_id()
        insert_new_url(short_id, url, username)
        return jsonify({"id": short_id}), 201

    @app.route("/", methods=["GET"])
    def list_urls():
        """ 
        Returns ids created by user (authenticated)
        """
        username = retrieve_username_from_token()
        if not username:
            return "", 403
        
        #Users now only see their own urls
        user_keys = ids_user(username)
        
        return jsonify({
            "values": user_keys if user_keys else None
        }), 200

    @app.route("/", methods=["DELETE"])
    def delete():
        """
        Delete endpoint. Requires authentication
        """
        username = retrieve_username_from_token()
        if not username:
            return "", 403
        
        return "", 404

    @app.route("/<string:id>", methods=["GET"])
    def get_url(id):
        """
        Returns long url associated with short url. Increments click counter.
        """
        row = get_id_by_url(id)
        if not row:
            return "", 404
        increment_clicks(id)

        return jsonify({"value": row[0]}), 301

    @app.route("/<string:id>", methods=["PUT"])
    def update_url(id):
        """
        Updates url for given short ID.
        """

        username = retrieve_username_from_token()
        if not username:
            return "", 403
        
        row = get_id_by_url(id)
        if not row:
            return "", 404

        owner = row[2]
        if owner != username:
            return "", 403


        # Try to parse JSON body, fallback to raw data if JSON parsing fails
        data = request.get_json(silent=True)
        if data is None and request.data:
            try:
                data = json.loads(request.data.decode("utf-8"))
            except Exception:
                data = None

        #Check if data is dict
        if not isinstance(data, dict):
            return bad_request()
        
        url = data.get("url") or data.get("value")

        #Check if url is valid
        if not url or not is_valid_url(url):
            return bad_request()
        
        #Check if url already exists and is not the same as the current url
        if does_url_exist(url,id):
            return bad_request("url exists already")
        update_url_in_db(id, url)

        return "", 200

    @app.route("/<string:id>", methods=["DELETE"])
    def delete_url(id):
        """
        Deletes short id. Only owner can delete.
        """

        username = retrieve_username_from_token()
        if not username:
            return "", 403
        
        row = get_id_by_url(id)
        if not row:
            return "", 404

        owner = row[2]
        if "owner" != username:
            return "", 403

        delete_url(id)
        return "", 204
    
    @app.route("/<string:id>/stats", methods=["GET"])
    def get_stats(id):
        """
        Returns statistics for short ID (click count).
        """
        row = get_id_by_url(id)
        if not row:
            return "", 404
        
        url, clicks, owner = row
        return jsonify({"id": id, 
                        "url": url,
                        "clicks": clicks}), 200
    
