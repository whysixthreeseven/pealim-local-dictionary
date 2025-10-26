# System-management library:
import os


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
MODULES DIRECTORIES BLOCK

"""


# Generating valid root path:
_ROOT_PATH: str = os.path.dirname(__file__)

# Directories path variables:
_FOLDER_DATABASE_NAME: str = "database"
_FOLDER_DATABASE_PATH: str = os.path.join(_ROOT_PATH, _FOLDER_DATABASE_NAME)
_FOLDER_UTILITIES_NAME: str = "utilities"
_FOLDER_UTILITIES_PATH: str = os.path.join(_ROOT_PATH, _FOLDER_UTILITIES_NAME)
_FOLDER_TEMPLATES_NAME: str = "templates"
_FOLDER_TEMPLATES_PATH: str = os.path.join(_ROOT_PATH, _FOLDER_TEMPLATES_NAME)
_FOLDER_COMPONENTS_NAME: str = "components"
_FOLDER_COMPONENTS_PATH: str = os.path.join(_FOLDER_TEMPLATES_PATH, _FOLDER_COMPONENTS_NAME)
_FOLDER_STATIC_NAME: str = "static"
_FOLDER_STATIC_PATH: str = os.path.join(_ROOT_PATH, _FOLDER_STATIC_NAME)
_FOLDER_CSS_NAME: str = "css"
_FOLDER_CSS_PATH: str = os.path.join(_FOLDER_STATIC_PATH, _FOLDER_CSS_NAME)
_FOLDER_JS_NAME: str = "js"
_FOLDER_JS_PATH: str = os.path.join(_FOLDER_STATIC_PATH, _FOLDER_JS_NAME)
_FOLDER_IMAGES_NAME: str = "images"
_FOLDER_IMAGES_PATH: str = os.path.join(_FOLDER_STATIC_PATH, _FOLDER_IMAGES_NAME)
_FOLDER_FONTS_NAME: str = "fonts"
_FOLDER_FONTS_PATH: str = os.path.join(_FOLDER_STATIC_PATH, _FOLDER_FONTS_NAME)

# Database filename and -path variables:
_DB_COMMON_FILENAME: str = "common.db"
_DB_COMMON_FILEPATH: str = os.path.join(_FOLDER_DATABASE_PATH, _DB_COMMON_FILENAME)

# Collection filename and -path variables:
_JSON_COLLECTION_FILENAME: str = "dict_collection.json"
_JSON_COLLECTION_FILEPATH: str = os.path.join(_FOLDER_UTILITIES_PATH, _JSON_COLLECTION_FILENAME)
_JSON_MISSING_FILENAME: str = "dict_missing.json"
_JSON_MISSING_FILEPATH: str = os.path.join(_FOLDER_UTILITIES_PATH, _JSON_MISSING_FILENAME)


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
SETTINGS CLASS INSTANCE BLOCK

"""


class SETTINGS:
    """
    TODO: Create a docstring.
    """
    
    # Application configuration:
    APP_NAME:    str  = "PEALIM-LOCAL-DICTIONARY"
    APP_VERSION: str  = "0.1t"
    APP_UPDATED: str  = "2025.10.26"
    APP_ROOT:    str  = _ROOT_PATH
    APP_HOST:    str  = "0.0.0.0"
    APP_PORT:    int  = 5001            # <- for MacOS
    APP_DEBUG:   bool = True
    APP_RELOAD:  bool = True
    
    # Session configuration:
    SESSION_PERMANENT:  bool = True
    SESSION_REMOVE_LOG: bool = True
    SESSION_KEY:        str  = "0"
    
    # SQL Alchemy extension configuration:
    SQLALCHEMY_DATABASE_URI:        str = f"sqlite:///{os.path.abspath(_DB_COMMON_FILEPATH)}"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # Folders configuration:
    FOLDER_DATABASE_PATH:     str = _FOLDER_DATABASE_PATH       # /database/
    FOLDER_UTILITIES_PATH:    str = _FOLDER_UTILITIES_PATH      # /utilities/
    FOLDER_TEMPLATES_PATH:    str = _FOLDER_TEMPLATES_PATH      # /templates/
    FOLDER_COMPONENTS_PATH:   str = _FOLDER_COMPONENTS_PATH     # /templates/components/
    FOLDER_STATIC_PATH:       str = _FOLDER_STATIC_PATH         # /static/
    FOLDER_CSS_PATH:          str = _FOLDER_CSS_PATH            # /static/css/
    FOLDER_JS_PATH:           str = _FOLDER_JS_PATH             # /static/js/
    FOLDER_IMAGES_PATH:       str = _FOLDER_IMAGES_PATH         # /static/images/
    FOLDER_FONTS_PATH:        str = _FOLDER_FONTS_PATH          # /static/fonts/
    
    # Database and collection configuration:
    DATABASE_FILEPATH:        str = _DB_COMMON_FILEPATH
    JSON_COLLECTION_FILEPATH: str = _JSON_COLLECTION_FILEPATH
    JSON_MISSING_FILEPATH:    str = _JSON_MISSING_FILEPATH
    
