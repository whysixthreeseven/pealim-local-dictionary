# Flask-related imports:
from flask import Blueprint, render_template, request
from typing import Any

# Settings and database imports:
from configuration import SETTINGS
from utilities.database import DATABASE
from utilities.database.models.word import Word


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
BLUEPRINT AND VARIABLES BLOCK

"""


# Generating blueprint:
DICTIONARY_BLUEPRINT: Blueprint = Blueprint(
    name="dictionary",
    import_name=__name__,
    template_folder=SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder=SETTINGS.FOLDER_STATIC_PATH,
)

# Getting constants:
DICTIONARY_PAGE_URL: str = "/dictionary"
DICTIONARY_PAGE_HTML: str = "dictionary.html"
WORDS_PER_PAGE: int = 100


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@DICTIONARY_BLUEPRINT.route(rule = DICTIONARY_PAGE_URL, methods = ["GET"])
def dictionary() -> str:
    """
    Display dictionary words with pagination.
    """

    # Getting page number from query parameters, default to 1
    page = request.args.get('page', 1, type = int)
    
    # Calculate pagination
    total_words = DATABASE.session.query(Word).count()
    total_pages = (total_words + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE      # <- Ceiling division
    
    # Ensure page is within valid range
    page: int = max(1, min(page, total_pages))
    
    # Get words for current page
    word_entry_list = DATABASE.session.query(Word)\
        .order_by(Word.INDEX)\
        .offset((page - 1) * WORDS_PER_PAGE)\
        .limit(WORDS_PER_PAGE)\
        .all()
    
    # Preparing pagination data:
    pagination = {
        'current_page': page,
        'total_pages':  total_pages,
        'total_words':  total_words,
        'has_prev':     page > 1,
        'has_next':     page < total_pages,
        'prev_page':    page - 1,
        'next_page':    page + 1,
        }
    
    # Prepare template context
    context: dict[str, Any] = {
        'words': word_entry_list,
        'pagination': pagination,
        }
    
    # Generating page route:
    page_route: str = render_template(
        DICTIONARY_PAGE_HTML, 
        **context
        )
    
    # Returning:
    return page_route

