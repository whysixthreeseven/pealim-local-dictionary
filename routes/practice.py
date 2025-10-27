# Flask-related imports:
from flask import Blueprint, render_template, request, redirect, url_for, flash
from typing import Any

# Settings and database imports:
from configuration import SETTINGS
from utilities.database import DATABASE
from utilities.database.models.input import Input


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
BLUEPRINT AND VARIABLES BLOCK
"""


# Generating blueprint:
PRACTICE_BLUEPRINT: Blueprint = Blueprint(
    name = "practice",
    import_name = __name__,
    template_folder = SETTINGS.FOLDER_TEMPLATES_PATH,
    static_folder = SETTINGS.FOLDER_STATIC_PATH,
    )

# Constants:
PRACTICE_PAGE_URL: str = "/practice"
PRACTICE_PAGE_HTML: str = "practice.html"
WORDS_PER_PAGE: int = 100


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ROUTING AND LOGIC BLOCK
"""


@PRACTICE_BLUEPRINT.route(rule = PRACTICE_PAGE_URL, methods = ["GET"])
def practice() -> str:
    """
    TODO: Create a docstring.
    """

    # Getting page number from query parameters, default = 1:
    page: int = request.args.get("page", 1, type=int)

    # Counting all Input entries:
    total_inputs: int = DATABASE.session.query(Input).count()
    total_pages: int = (total_inputs + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE  # Ceiling division

    # Ensuring page is valid:
    page = max(1, min(page, total_pages if total_pages else 1))

    # Query subset of inputs for the current page:
    input_list = (
        DATABASE.session.query(Input)
        .order_by(Input.ID)
        .offset((page - 1) * WORDS_PER_PAGE)
        .limit(WORDS_PER_PAGE)
        .all()
        )

    # Preparing pagination data:
    pagination = {
        "current_page": page,
        "total_pages": total_pages,
        "total_words": total_inputs,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1,
        "next_page": page + 1,
        }

    # Template context:
    context: dict[str, Any] = {
        "inputs": input_list,
        "pagination": pagination,
        }

    # Generating page route:
    page_route: str = render_template(
        PRACTICE_PAGE_HTML, 
        **context
        )

    # Returning:
    return page_route


# --------------------------------------------------------------------------------------------------


@PRACTICE_BLUEPRINT.route(rule=f"{PRACTICE_PAGE_URL}/add", methods=["POST"])
def add_word() -> Any:
    """
    TODO: Create a docstring.
    """

    # Collecting form data:
    word_he = request.form.get("WORD_HE", "").strip()
    stem_he = request.form.get("STEM_HE", "").strip()
    transcription_ru = request.form.get("TRANSCRIPTION_RU", "").strip()
    translation_ru = request.form.get("TRANSLATION_RU", "").strip()
    pos_ru = request.form.get("POS_RU", "").strip()
    inf_ru = request.form.get("INF_RU", "").strip()

    # Assertion control:
    if not word_he:
        flash("Hebrew word is required.", "error")
        return redirect(url_for("practice.practice"))

    # Creating a new Input entry
    new_entry = Input(
        WORD_HE = word_he,
        STEM_HE = stem_he,
        TRANSCRIPTION_RU = transcription_ru,
        TRANSLATION_RU = translation_ru,
        POS_RU = pos_ru,
        INF_RU = inf_ru,
        )

    # Add and commit to database
    DATABASE.session.add(new_entry)
    DATABASE.session.commit()

    # Generating page route:
    page_route: str = redirect(
        url_for("practice.practice")
        )

    # Returning: 
    return page_route


# --------------------------------------------------------------------------------------------------


@PRACTICE_BLUEPRINT.route(rule=f"{PRACTICE_PAGE_URL}/<int:id>", methods=["GET"])
def practice_detail(id: int) -> str:
    """
    Displays a detailed view for a single Input entry.
    """

    # Fetch entry by ID
    input_entry = DATABASE.session.query(Input).get(id)
    if not input_entry:
        flash("Entry not found.", "error")
        return redirect(url_for("practice.practice"))

    # Render detail page (you can later create practice_detail.html)
    return render_template("practice/practice_detail.html", entry=input_entry)
