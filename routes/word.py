# Flask-related imports:
from flask import abort, Blueprint, render_template, session 
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
WORD_BLUEPRINT: Blueprint = Blueprint(
    name = "word",
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
WORD_PAGE_URL: str = "/dictionary/<language>/<int:word_index>"
WORD_PAGE_HTML: str = "word.html"
SUPPORTED_LANGUAGES: set = {'ru', 'en', 'he'}


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@WORD_BLUEPRINT.route(rule = WORD_PAGE_URL, methods = ["GET"])
def word_detail(language: str, word_index: int) -> str:
    """
    Display detailed word page for a specific language and word index.
    
    Args:
        lang: Language code ('ru', 'en', 'he')
        word_index: Word index number
        
    Returns:
        Rendered word detail page
    """
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        abort(404, description="Language not supported")
        
    # Saving last used language:
    session["LANG_USED"] = language
    
    # Getting word from database:
    word = DATABASE.session.query(Word)\
        .filter(Word.INDEX == word_index)\
        .first()
    
    # Checking if word exists:
    if not word:
        abort(404, description="Word not found")
    
    # Getting the appropriate container and translation based on language:
    container_attr = f'HTML_CONTAINER_LANG_{language.upper()}'
    translation_attr = f'TRANSLATION_LANG_{language.upper()}'
    
    container_html = getattr(word, container_attr, '')
    translation = getattr(word, translation_attr, '')
    
    # Check if container exists for this language
    if not container_html:
        abort(404, description=f"Word content not available in {language}")
    
    # Preparing template context:
    context: dict[str, Any] = {
        'word': word,
        'language': language,
        'container_html': container_html,
        'translation': translation,
        'hebrew_word': word.TRANSLATION_LANG_HE,
        }
    
    # Generating page route:
    page_route: str = render_template(
        template_name_or_list = WORD_PAGE_HTML, 
        **context
        )
    
    return page_route