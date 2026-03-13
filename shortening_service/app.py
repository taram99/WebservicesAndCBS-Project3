from flask import Flask
from routes import register_routes
from database2 import init_db

def create_app():
    app = Flask(__name__)
    #Registers all routes
    register_routes(app)
    return app
#Runs if file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000) #Debug enables automatic reload
