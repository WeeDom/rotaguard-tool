from flask import Flask
from .db import db
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os
from .api import api

migrate = Migrate()
bcrypt = Bcrypt()

def create_app(database_uri=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a-very-secret-key' # Change this in production
    if database_uri is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    api.init_app(app)

    # Import and register namespaces inside the factory
    from .auth_api import ns as auth_ns
    from .roles_api import ns as roles_ns
    from .users_api import api as users_ns
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(roles_ns, path='/roles')
    api.add_namespace(users_ns, path='/users')


    # Register main blueprint for HTML routes
    from .main.routes import main_bp
    app.register_blueprint(main_bp)

    return app
