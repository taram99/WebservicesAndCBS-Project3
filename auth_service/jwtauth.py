import base64
import hmac
import hashlib
import json
import os

#print(os.environ.get("JWT_SECRET"))

SECRET = os.environ.get("JWT_SECRET")
#print("SECRET:", SECRET)

def base64UrlEncode(data):
    """
    Encodes Python library into Base64 safe string. Converts dictionary to JSON string.
    Encodes it to bytes and applies URL safe encoding. Also removes padding characters.

    data (dict): the dictionary to encode
    """
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")
    

def generating_jwt(username):
    """
    Generates signed JWT web token for given username. JWT consits of header, payload, 
    signature (preventing temperaring).

    username(str): username to embed in token.
    """
    #alg is the signing algorithm
    header = {
    "alg": "HS256",
    "typ": "JWT"
    }
    #now Json is base64 encoded

    payload = {"username": username}


    header_b64 =  base64UrlEncode(header) 
    payload_b64 = base64UrlEncode(payload)

    message = f"{header_b64}.{payload_b64}"

    signature = hmac.new(SECRET.encode(), message.encode(), hashlib.sha256).digest()

    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{message}.{signature_b64}"


#function to make sure username in token cannot be changed
def validating_jwt(token):
    """
    Validates JWT web token. First splitted into payload, header, signature. 
    Then recomputed to expected signature using the secret key, then the signatures are compared.
    If valid, decode payload and return username. Return None otherwise.

    token(str): JWT string to validate
    """
    try:
        #Split token
        header_b64, payload_b64, signature_b64 = token.split(".")
        #Signed message
        message = f"{header_b64}.{payload_b64}"
        #Recompute what signature should be
        expected_signature = hmac.new(
            SECRET.encode(), 
            message.encode(), 
            hashlib.sha256
            ).digest()
        #Encode it and convert to base64 format
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip("=")
        #Compare signatures
        if signature_b64 != expected_signature_b64:
            return None
        #If signature is valid decode payload
        payload_json = base64.urlsafe_b64decode(
            payload_b64 + "=="
            ).decode()
        #Extract username out of token
        payload = json.loads(payload_json)

        return payload.get("username")
    

    except Exception:
        return None
    




