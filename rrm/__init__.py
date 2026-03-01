import os

from flask import Flask
from dotenv import load_dotenv


load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_URL=os.environ.get('DATABASE_URL'),
        SEMAIL=os.environ.get('SEMAIL'),
        SPASSWORD=os.environ.get('SPASSWORD')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    # initialize layout
    from .db import query_all, execute
    from .layout import init_layout
    with app.app_context():
        init_layout(query_all)

    # register enquiry functions
    from .reminder import sendReminder
    with app.app_context():
        sendReminder(query_all, execute, app)
    
    # register blueprints
    from . import student
    app.register_blueprint(student.bp)
    app.add_url_rule('/', endpoint='student')

    from . import admin
    app.register_blueprint(admin.bp)

    return app