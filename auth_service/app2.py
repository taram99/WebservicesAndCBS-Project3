from flask import Flask
from routes2 import auth_routes #Contains all authentication routes
from database import init_db


app = Flask(__name__)
#Connects routes defined in routes2.py to this app
app.register_blueprint(auth_routes)
#Verify service is running
def home():
    return "Auth service running"

#Runs if this file is executed directly
if __name__ == "__main__":
    init_db() #ensures table is created when service starts
    app.run(host="0.0.0.0", port=8001) #Debug enables automatic reload