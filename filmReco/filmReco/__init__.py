from flask import Flask

from .main.login import auth
from .main.routes import main

from .extensions import mongo

def create_app():
    app = Flask(__name__)

    app.config['MONGO_URI']="mongodb+srv://plop:plop@todoapp.kledxsi.mongodb.net/critics?retryWrites=true&w=majority"
    mongo.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app

#if __name__ == __main__:
#    app.run()
