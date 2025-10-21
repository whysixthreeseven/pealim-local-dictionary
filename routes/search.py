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
SEARCH_BLUEPRINT: Blueprint = Blueprint(
    name = "search", 
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
SEARCH_PAGE_URL: str = "/search"
SEARCH_PAGE_HTML: str = "search.html"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@SEARCH_BLUEPRINT.route(rule = SEARCH_PAGE_URL)
def search() -> str:

    # Getting route page rendered:
    page_route: str = render_template(
        template_name_or_list = SEARCH_PAGE_HTML
        )
    
    # Returning:
    return page_route