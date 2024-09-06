import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #CORS(app, resources={r"/*": {"origins": "*"}})
    #CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500", "null"]}})
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        JWT_SECRET_KEY='jwt_dev',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=3),
        DATABASE=os.path.join(app.instance_path, 'besked_central.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    print(
        f"JWT_ACCESS_TOKEN_EXPIRES: {app.config['JWT_ACCESS_TOKEN_EXPIRES']}")
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .src import db
    db.init_app(app)

    from .src import auth
    app.register_blueprint(auth.bp)

    from .src.users import users
    app.register_blueprint(users.bp)

    from .src.tracks import tracks
    app.register_blueprint(tracks.bp)
    from .src.tracks import tracks_api
    app.register_blueprint(tracks_api.bp)

    from .src.events import events
    app.register_blueprint(events.bp)
    from .src.events import events_api
    app.register_blueprint(events_api.bp)

    from .src import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    JWTManager(app)

    return app
