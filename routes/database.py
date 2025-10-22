# Default logger import:
import logging
log = logging.getLogger(__name__)

# Flask-related imports:
from flask import Blueprint
from flask import render_template, redirect, request, session

# Typing and annotations import:
from typing import Any

# Settings import:
from configuration import SETTINGS

# Database and related import:
from utilities.database import DATABASE
from utilities import convert, verification



"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
BLUEPRINT AND VARIABLES BLOCK

"""

# Generating blueprint:
DATABASE_BLUEPRINT: Blueprint = Blueprint(
    name = "database", 
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
DATABASE_PAGE_URL: str = "/database"
DATABASE_PAGE_HTML: str = "database.html"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@DATABASE_BLUEPRINT.route(rule=DATABASE_PAGE_URL, methods=["GET", "POST"])
def database() -> str:
    """
    Handle database status page with data verification.
    """

    # Default values:
    rebuild_success: bool = False
    rebuild_entry_count: int = 0

    # POST request handling:
    if request.method == "POST":

        # Data verification:
        if "check_data" in request.form:
            log.info("Check Data requested - running verification...")
            verification.verify_data()

        # Data rebuilding:
        elif "rebuild_database" in request.form:
                log.info("Rebuild Database button clicked - starting rebuild process...")
                
                # Attempting to rebuild:
                try:

                    # Delete all entries from words table
                    from utilities.database.models.word import Word
                    deleted_count = Word.query.delete()
                    DATABASE.session.commit()
                    log.info(f"Deleted {deleted_count} entries from database")
                    
                    # Rebuild from JSON
                    converter = convert.Converter(
                         json_filepath = SETTINGS.JSON_COLLECTION_FILEPATH
                         )
                    rebuild_entry_count = converter.run()  # This should return the number of entries added
                    
                    # Update verification data:
                    verification.verify_data()
                    rebuild_success = True

                    # Logging:
                    log.info(f"Database rebuilt successfully with {rebuild_entry_count} entries")
                    
                # Handling exceptions and rolling back:
                except Exception as exception_error:
                    DATABASE.session.rollback()
                    rebuild_success = False
                    log.error(f"Database rebuild failed: {exception_error}")
    
    # Preparing template context from session data:
    context: dict[str, Any] = {
        'json_status': verification.status_json(),
        'json_count': session.get('JSON_DATA_COUNT', 0),
        'database_status': verification.status_database(),
        'database_count': session.get('DATABASE_ENTRY_COUNT', 0),
        'rebuild_success': rebuild_success,
        'rebuild_count': rebuild_entry_count
        }

    # Generating page routing:
    page_route: str = render_template(
        template_name_or_list = DATABASE_PAGE_HTML,
        **context
        )
    
    # Getting route page rendered WITH CONTEXT:
    return page_route
