from flask import Flask
from routes2 import auth_routes #Contains all authentication routes

app = Flask(__name__)
#Connects routes defined in routes2.py to this app
app.register_blueprint(auth_routes)
#Verify service is running
def home():
    return "Auth service running"

#Runs if this file is executed directly
if __name__ == "__main__":
    app.run(port=8001, debug=True) #Debug enables automatic reload