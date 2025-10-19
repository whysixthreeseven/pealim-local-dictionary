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
SELECTED_BLUEPRINT: Blueprint = Blueprint(
    name = "selected", 
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Getting constants:
SELECTED_PAGE_URL: str = "/selected"
SELECTED_PAGE_HTML: str = "selected.html"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK

"""


@SELECTED_BLUEPRINT.route(rule = SELECTED_PAGE_URL)
def selected() -> str:

    # Getting route page rendered:
    page_route: str = render_template(
        template_name_or_list = SELECTED_PAGE_HTML
        )
    
    # Returning:
    return page_route