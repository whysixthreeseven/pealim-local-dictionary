"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
LOGGER SETUP

"""


# Default logger import:
import logging as log

# System-management import:
import sys

# Forcing UTF-8 encoding for Windows:
if sys.platform == "win32":
    if isinstance(sys.stdout, type(sys.__stdout__)) and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding = 'UTF-8')
    if isinstance(sys.stderr, type(sys.__stderr__)) and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding = 'UTF-8')

# Logger configuration variables:
log_filepath: str = "utilities/application.log"
log_format: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
log_handlers: list = [
    log.FileHandler(log_filepath, encoding = "UTF-8"),
    log.StreamHandler()
    ]

# Setting up basic configuration:
log.basicConfig(
    level = log.DEBUG,
    format = log_format,
    handlers = log_handlers,
    encoding = "UTF-8"
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATING AND SETTING UP APPLICATION

"""

# Flask library and related import:
from flask import Flask

# Settings container import:
from configuration import SETTINGS
from utilities.namespace import (
    SESSION_PERMANENT, 
    SQLALCHEMY_DATABASE_URI, 
    SQLALCHEMY_TRACK_MODIFICATIONS, 
    )


# Creating Flask application:
application = Flask(
    import_name     = SETTINGS.APP_NAME,
    static_folder   = SETTINGS.FOLDER_STATIC_PATH,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    )
application.secret_key = SETTINGS.SESSION_KEY

# Logging:
log.info("Flask application started")

# Configuring application:
application.config[SESSION_PERMANENT] = SETTINGS.SESSION_PERMANENT
application.config[SQLALCHEMY_DATABASE_URI] = SETTINGS.SQLALCHEMY_DATABASE_URI
application.config[SQLALCHEMY_TRACK_MODIFICATIONS] = SETTINGS.SQLALCHEMY_TRACK_MODIFICATIONS

# Logging:
log.info("Flask application configured")


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DATABASE SETUP CREATION

"""


# Database import:
from utilities.database import DATABASE
from utilities.database import environment

# Utilities import:
from utilities import verification


# Creating database:
DATABASE.init_app(
    app = application
    )

# Logging:
log.info("Database instance created")

# Database model import:
from utilities.database.models.word import Word

# Initializing database:
environment.initialize_database_environment()
with application.app_context():
    DATABASE.create_all()
    log.info("Database tables created")

    
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
REGISTERING BLUEPRINTS

"""


# Importing blueprints:
from routes.home import HOME_BLUEPRINT
from routes.dictionary import DICTIONARY_BLUEPRINT
from routes.database import DATABASE_BLUEPRINT
from routes.favourites import FAVOURITES_BLUEPRINT
from routes.random import RANDOM_BLUEPRINT
from routes.search import SEARCH_BLUEPRINT
from routes.word import WORD_BLUEPRINT
# from routes.practice.input import INPUT_BLUEPRINT
# from routes.practice.view import VIEW_BLUEPRINT


# Registering blueprints:
application.register_blueprint(blueprint = HOME_BLUEPRINT)
application.register_blueprint(blueprint = DICTIONARY_BLUEPRINT)
application.register_blueprint(blueprint = DATABASE_BLUEPRINT)
application.register_blueprint(blueprint = FAVOURITES_BLUEPRINT)
application.register_blueprint(blueprint = RANDOM_BLUEPRINT)
application.register_blueprint(blueprint = SEARCH_BLUEPRINT)
application.register_blueprint(blueprint = WORD_BLUEPRINT)
# application.register_blueprint(blueprint = INPUT_BLUEPRINT)
# application.register_blueprint(blueprint = VIEW_BLUEPRINT)

# Logging:
log.info("Routing blueprints registered")


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
APPLICATION RUN BLOCK

"""


def application_run() -> None:
    """
    TODO: Create a docstring.
    """

    # Starting application with settings variables:
    application.run(
        debug        = SETTINGS.APP_DEBUG, 
        host         = SETTINGS.APP_HOST, 
        port         = SETTINGS.APP_PORT,
        use_reloader = SETTINGS.APP_RELOAD
        )
    
    # Logging:
    log.info("Flask application is now running")


if __name__ == "__main__":
    application_run()

