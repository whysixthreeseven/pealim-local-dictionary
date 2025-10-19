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
INDEX_BLUEPRINT: Blueprint = Blueprint(
    name = "index", 
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
INDEX_PAGE_URL: str = "/"
INDEX_PAGE_HTML: str = "index.html"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@INDEX_BLUEPRINT.route(rule = INDEX_PAGE_URL)
def index() -> str:

    # Getting route page rendered:
    page_route: str = render_template(
        template_name_or_list = INDEX_PAGE_HTML
        )
    
    # Returning:
    return page_route