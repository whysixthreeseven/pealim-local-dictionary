# Default logger import:
import logging
log = logging.getLogger(__name__)

# System-management library:
import os

# Local settings import:
from configuration import SETTINGS


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DATABASE ENVIRONMENT SETUP FUNCTIONS BLOCK

"""


def __ensure_database_root() -> None:
    """
    Ensures that the root database folder exists in the filesystem. If the folder is missing, it 
    is automatically created.

    ## Behavior:
    - Retrieves the database folder path from `SETTINGS.FOLDER_DATABASE_PATH`;
    - Creates the folder if it does not exist;
    - Logs all actions and outcomes.
    """
    
    # Creating database folder if it does not exists:
    database_folder_path: str = SETTINGS.FOLDER_DATABASE_PATH
    os.makedirs(
        name = database_folder_path,
        exist_ok = True
        )
    
    # Logging:
    log.info(f"Ensured database root at: {SETTINGS.FOLDER_DATABASE_PATH}")
    
    
def __ensure_database_files() -> None:
    """
    Ensures that all required SQLite database files exist within the database folder. If a file is 
    missing, it is created as an empty file.

    ## Behavior:
    - Checks for existence of each file path defined in `SETTINGS`;
    - Creates missing files using `open(..., mode='x')`;
    - Logs both creation and verification results.
    """
    
    # Acquiring all database filepaths and making a list to create:
    database_object_filepath_list: tuple[str, ...] = (
        SETTINGS.DATABASE_FILEPATH,
        )
    for database_object_filepath in database_object_filepath_list:
        database_object_exists: bool = os.path.exists(
            path = database_object_filepath
            )
        
        # Creating database file object if it doesn't exist:
        if not database_object_exists:
            open(file = database_object_filepath, mode = "x")
            
            # Logging:
            log.info(f"Created new database object at {database_object_filepath}")
    
    # Logging:
    log.info(f"Ensured database files at: {SETTINGS.FOLDER_DATABASE_PATH}")
    

def initialize_database_environment() -> None:
    """
    Initializes the database environment before the application starts. This includes verifying 
    that the root database folder and all expected database files exist — creating them if they 
    do not.

    ## Behavior:
    - Calls `__ensure_database_root()` to create the root folder if needed;
    - Calls `__ensure_database_files()` to create required `.db` files;
    - Logs the initialization process and completion.

    ## Example:
        >>> initialize_database_environment()
        # Logs:
        #   "Initializing database environment..."
        #   "Ensured database root at: ./database"
        #   "Ensured database files at: ./database"
        #   "Database environment is initialized and ready"
    """

    # Logging:
    log.info("Initializing database environment...",)
    
    # Ensuring database root folder and files exist (and/or creating new):
    __ensure_database_root()
    __ensure_database_files()

    # Logging:
    log.info("Database environment is initialized and ready")
    
