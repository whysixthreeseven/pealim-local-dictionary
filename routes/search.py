# Default logger import:
import logging
log = logging.getLogger(__name__)

# Flask-related imports:
from flask import Blueprint
from flask import render_template, redirect, request, session
from sqlalchemy import func

# Settings import:
from configuration import SETTINGS

# Database-related import:
from utilities.database import DATABASE
from utilities.database.models.word import Word


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
BLUEPRINT AND VARIABLES BLOCK

"""

# Generating blueprint:
SEARCH_BLUEPRINT: Blueprint = Blueprint(
    name = "search", 
    import_name = __name__,
    url_prefix = "/search",
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
SEARCH_PAGE_URL: str = "/"
SEARCH_PAGE_HTML: str = "search.html"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@SEARCH_BLUEPRINT.route("/", methods = ["GET"])
def search():
    """
    TODO: Create a docstring.
    """

    # Getting query string:
    query_input = request.args.get("query", "").strip()
    
    # Rendering empty results page if query is empty:
    if not query_input:
        page_route: str = render_template(
            template_name_or_list = "search.html", 
            query = None, 
            results = [], 
            language = None
            )
        return page_route 

    # Preparing search pattern for partial, case-insensitive match:
    search_pattern = f"%{query_input.lower()}%"
    search_results: list[str] = []
    search_language: str = None

    # Attempting to search:
    try:
        
        # English language:
        search_results = (
            Word.query.filter(
                func.lower(func.cast(Word.SEARCH_LANG_EN, DATABASE.String)).like(search_pattern)
                ).all()
            )
        if search_results:
            search_language = "en"
            log.info(f"Found {len(search_results)} English results for '{query_input}'")

        #  Russian language:
        if not search_results:
            search_results = (
                Word.query.filter(
                    func.lower(func.cast(Word.SEARCH_LANG_RU, DATABASE.String)).like(search_pattern)
                    ).all()
                )
            if search_results:
                search_language = "ru"
                log.info(f"Found {len(search_results)} Russian results for '{query_input}'")

        # Hebrew language:
        if not search_results:
            search_results = (
                Word.query.filter(
                    func.lower(func.cast(Word.SEARCH_LANG_HE, DATABASE.String)).like(search_pattern)
                    ).all()
                )
            if search_results:
                search_language = "he"
                log.info(f"Found {len(search_results)} Hebrew results for '{query_input}'")

    # Handling exceptions and errors:
    except Exception as e:
        log.error(f"Search failed for '{query_input}': {e}")
        search_results: list[str] = []
        search_language: str | None = None

    # Page routing:
    page_route: str = render_template(
        "search.html",
        query=query_input,
        results=search_results,
        language=search_language
        )
    
    # Returning:
    return page_route

