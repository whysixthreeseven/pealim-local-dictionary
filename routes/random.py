# Default logger import:
import logging
log = logging.getLogger(__name__)

# Flask-related imports:
from flask import Blueprint
from flask import redirect, render_template, session, url_for

# Random import:
from random import randint

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
RANDOM_BLUEPRINT: Blueprint = Blueprint(
    name = "random", 
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
RANDOM_PAGE_URL: str = "/random"
RANDOM_PAGE_HTML: str = "random.html"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@RANDOM_BLUEPRINT.route(RANDOM_PAGE_URL)
def random():
    """
    Redirects to a random word entry.
    """

    # Checking database entry count:
    database_attached: bool = session.get('DATABASE_ATTACHED', False)
    database_entry_count: int = session.get('DATABASE_ENTRY_COUNT', 0)
    
    # Rerouting to /database on empty database check:
    if not database_attached or not database_entry_count:
        log.warning("Random page requested, but database not attached or empty")
        page_route: str = render_template(
            template_name_or_list = "database.html",
            )
        return page_route

    # Random offset selection:
    random_index: int = randint(0, database_entry_count - 1)
    random_word: Word = DATABASE.session.query(Word).offset(random_index).first()
    
    # Rerouting to /database on bad query:
    if not random_word:
        log.error("Random word query returned None.")
        page_route: str = render_template(
            template_name_or_list = "database.html",
            )
        return page_route
    
    # Last used language:
    language_used: str = session.get("LANG_USED", "en")

    # Generating page route:
    page_route: str = redirect(
        url_for(
            endpoint = "word.word_detail",
            language = language_used,
            word_index = random_word.INDEX
            )
        )

    # Returning:
    return page_route

