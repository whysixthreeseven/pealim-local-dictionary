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


@DATABASE_BLUEPRINT.route(rule = DATABASE_PAGE_URL)
def database() -> str:

    # Getting route page rendered:
    page_route: str = render_template(
        template_name_or_list = DATABASE_PAGE_HTML
        )
    
    # Returning:
    return page_route