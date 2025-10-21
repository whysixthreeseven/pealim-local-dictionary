# Default logger import:
import logging
log = logging.getLogger(__name__)

# Flask session import:
from flask import session

# System-management library:
import os

# JSON-related library:
import json

# Local settings and session import:
from configuration import SETTINGS

# Database-related import:
from utilities.database import DATABASE
from sqlalchemy import func


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
FILE VERIFICATION FUNCTIONS

"""


def __verify_json_data_attached() -> bool:
    """
    TODO: Create a docstring.
    """
    
    # Verifying file existence:
    json_data_exists: bool = os.path.exists(
        path = SETTINGS.JSON_COLLECTION_FILEPATH
        )
    
    # Logging:
    log.info(f"JSON data attached: {json_data_exists}")
    
    # Returning:
    return json_data_exists


def __verify_database_attached() -> bool:
    """
    TODO: Create a docstring.
    """

    # Verifying file existance:
    database_exists: bool = os.path.exists(
        path = SETTINGS.DATABASE_FILEPATH
        )
    
    # Logging:
    log.info(f"Database attached: {database_exists}")
    
    # Returning:
    return database_exists


def __calc_database_entry_count() -> int:
    """
    Count the number of Word entries in the database. Performs a database query to count all Word 
    model instances in the words table. This provides the current state of the database for 
    comparison with JSON data.
    
    :return int: Number of Word entries in the database, or 0 if query fails.
    """

    # Attempting SQL Alchemy's native function for efficiency:
    try:
        from utilities.database.models.word import Word
        entry_count: int | None = DATABASE.session.query(func.count(Word.ID)).scalar()
        calc_result: int = entry_count or 0
        log.info(f"Database contains {entry_count} Word entries")

        # Returning:
        return calc_result
    
    # Returning 0 on a failed attempt to get entry count:
    except Exception as exception_error:
        log.error(f"Error counting database entries: {exception_error}")
        return 0
    

def __calc_json_data_entry_count(json_filepath: str = None) -> int:
    """
    Count the number of entries in the JSON dictionary data file.
    
    This function loads the JSON file and counts the total number of word entries (page indexes) 
    contained within it. Useful for verifying data completeness after scraping.
    
    :param str json_filepath: Path to the JSON file. If `None`, uses 
        `SETTINGS.JSON_COLLECTION_FILEPATH`
        
    :return int: Number of entries in the JSON file, or 0 if file doesn't exist or is invalid.
    """

    # Using default filepath if none provided
    if json_filepath is None:
        json_filepath = SETTINGS.JSON_COLLECTION_FILEPATH
    
    # Checking if file exists
    if not os.path.exists(json_filepath):
        log.error(f"JSON file not found: {json_filepath}")
        return 0
    
    # Attempting to open and read the file:
    try:
        with open(file = json_filepath, mode = 'r', encoding = 'UTF-8') as json_file:
            json_data = json.load(json_file)
        
        # Counting:
        entry_count = len(json_data)
        log.info(f"JSON data contains {entry_count} entries")

        # Returning:
        return entry_count
    
    # Handling exceptions and returning zero on a failed inspection:
    except (json.JSONDecodeError, UnicodeDecodeError) as exception_error:
        log.error(f"Error reading JSON file {json_filepath}: {exception_error}")
        return 0
    except Exception as exception_error:
        log.error(f"Unexpected error reading JSON file: {exception_error}")
        return 0


def verify_data() -> None:
    """
    Perform data verification and store results in Flask session.
    
    This function checks the availability and entry counts of both JSON data and database, then 
    stores the results in the Flask session for persistence across requests.
    """
    
    # Logging:
    log.info("Starting data verification process...")

    # Verification start:
    try:

        # Verifying JSON data:
        json_attached = __verify_json_data_attached()
        session['JSON_DATA_ATTACHED'] = json_attached
        if json_attached: 
            session['JSON_DATA_COUNT'] = __calc_json_data_entry_count()
        else:
            session['JSON_DATA_COUNT'] = 0
        
        # Verifying database entries:
        db_attached = __verify_database_attached()
        session['DATABASE_ATTACHED'] = db_attached
        if db_attached: 
            session['DATABASE_ENTRY_COUNT'] = __calc_database_entry_count()
        else:
            session['DATABASE_ENTRY_COUNT'] = 0

    # Handling exception/error:
    except Exception as e:
        log.error(f"Verification failed: {e}")

        # Seting default values on error:
        session['JSON_DATA_ATTACHED'] = False
        session['JSON_DATA_COUNT'] = 0
        session['DATABASE_ATTACHED'] = False
        session['DATABASE_ENTRY_COUNT'] = 0


def status_json() -> str:
    """
    Determine the status of JSON data based on verification results.
    
    :return str: Status: `'Ready'`, `'Async'`, or `'Missing'`
    """

    # Use get() with defaults to avoid KeyError
    json_attached = session.get('JSON_DATA_ATTACHED', False)
    json_data_count = session.get('JSON_DATA_COUNT', 0)
    database_entry_count = session.get('DATABASE_ENTRY_COUNT', 0)
    
    # Generating status:
    status = "Missing"
    if json_attached:
        if json_data_count > 0:
            if json_data_count == database_entry_count:
                status = "Ready"
            else:
                status = "Async"
    
    # Returning:
    return status


def status_database() -> str:
    """
    Determine the status of database based on verification results.
    
    :return str: Status: `'Ready'`, `'Async'`, or `'Missing'`
    """

    # Using get() with defaults to avoid KeyError:
    database_attached = session.get('DATABASE_ATTACHED', False)
    database_entry_count = session.get('DATABASE_ENTRY_COUNT', 0)
    json_data_count = session.get('JSON_DATA_COUNT', 0)
    
    # Generating status:
    status = "Missing"
    if database_attached:
        if database_entry_count > 0:
            if json_data_count == database_entry_count:
                status = "Ready"
            else:
                status = "Async"
    
    # Returnign:
    return status