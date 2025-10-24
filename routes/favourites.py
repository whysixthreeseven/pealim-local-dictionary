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
FAVOURITES_BLUEPRINT: Blueprint = Blueprint(
    name = "favourites", 
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
FAVOURITES_PAGE_URL: str = "/favourites"
FAVOURITES_PAGE_HTML: str = "favourites.html"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@FAVOURITES_BLUEPRINT.route(rule = FAVOURITES_PAGE_URL)
def favourites() -> str:

    # Getting route page rendered:
    page_route: str = render_template(
        template_name_or_list = FAVOURITES_PAGE_HTML
        )
    
    # Returning:
    return page_route