# Default logger import:
import logging
log = logging.getLogger(__name__)

# System-management library:
import os

# JSON-related library:
import json

# Local settings import:
from configuration import SETTINGS


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
FILE VERIFICATION FUNCTIONS

"""


def verify_json_collection() -> bool:
    """
    TODO: Create a docstring.
    """
    
    # Verifying file existence:
    json_collection_verified: bool = False
    json_collection_exists: bool = os.path.exists(
        path = SETTINGS.JSON_COLLECTION_FILEPATH
        )
    
    # Testing file entries:
    if json_collection_exists:
        with open(file = SETTINGS.JSON_COLLECTION_FILEPATH, mode = 'r', encoding = "UTF-8") as json_file:
            json_file_data = json.load(json_file)
        
        # Logging:
        log.info(f"JSON total entries: {len(json_file_data)}")
        
        # Checking for duplicates:
        json_data_count: int = len(json_file_data)
        json_set_count: int = len(set(json_file_data))
        if json_data_count != json_set_count:
            log.warning("JSON collection contains duplicate entries")
        else:
            json_collection_verified: bool = True
    
    # Returning:
    return json_collection_verified

