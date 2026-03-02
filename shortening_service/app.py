from flask import Flask
from routes import register_routes

def create_app():
    app = Flask(__name__)
    #Registers all routes
    register_routes(app)
    return app
#Runs if file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(port=8000, debug=True) #Debug enables automatic reload
