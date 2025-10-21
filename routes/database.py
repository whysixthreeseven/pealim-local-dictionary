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

# Utilities import:
from utilities import verification




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

    # Handling POST request (Check Data button clicked):
    if request.method == "POST" and "check_data" in request.form:
        log.info("Check Data requested - running verification...")
        verification.verify_data()
    
    # Preparing template context from session data:
    context: dict[str, Any] = {
        'json_status': verification.status_json(),
        'json_count': session.get('JSON_DATA_COUNT', 0),
        'database_status': verification.status_database(),
        'database_count': session.get('DATABASE_ENTRY_COUNT', 0),
        }

    # Generating page routing:
    page_route: str = render_template(
        template_name_or_list = DATABASE_PAGE_HTML,
        **context
        )
    
    # Getting route page rendered WITH CONTEXT:
    return page_route

