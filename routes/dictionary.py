# Flask-related imports:
from flask import Blueprint
from flask import render_template, redirect, request, session

# Settings import:
from configuration import SETTINGS


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
BLUEPRINT AND VARIABLES BLOCK

"""

# Generating blueprint:
DICTIONARY_BLUEPRINT: Blueprint = Blueprint(
    name = "dictionary", 
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
DICTIONARY_PAGE_URL: str = "/dictionary"
DICTIONARY_PAGE_HTML: str = "dictionary.html"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@DICTIONARY_BLUEPRINT.route(rule = DICTIONARY_PAGE_URL)
def dictionary() -> str:

    # Getting route page rendered:
    page_route: str = render_template(
        template_name_or_list = DICTIONARY_PAGE_HTML
        )
    
    # Returning:
    return page_route