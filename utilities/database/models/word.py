# Default logger import:
import logging
log = logging.getLogger(__name__)

# Database types:
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.orm import validates

# Typing and annotations import
from typing import Any, Literal, Optional

# HTML composition related imports:
from bs4 import BeautifulSoup
import re

# Database import:
from utilities.database import DATABASE

# Utilities import:
from utilities.database.models import context
from utilities.database import scripts


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
WORD DATABASE MODEL

"""


class Word(DATABASE.Model):
    """
    TODO: Create a docstring.
    """
    
    # Assigning table name:
    __tablename__: str = "words"
    
    # Core attributes:
    ID = Column(Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    INDEX = Column(Integer, nullable = False, unique = True)

    # Table injection attributes:
    HTML_CONTAINER_LANG_RU = Column(String, nullable = False)
    HTML_CONTAINER_LANG_EN = Column(String, nullable = False)
    HTML_CONTAINER_LANG_HE = Column(String, nullable = False)
    
    # Translation and transcribtion attributes::
    TRANSLATION_LANG_HE = Column(String, nullable = True)
    TRANSLATION_LANG_RU = Column(String, nullable = True)
    TRANSLATION_LANG_EN = Column(String, nullable = True)
    # TRANSCRIBTION_LANG_HE = Column(String, nullable = True)
    TRANSCRIBTION_LANG_RU = Column(String, nullable = True)
    TRANSCRIBTION_LANG_EN = Column(String, nullable = True)
    # SEARCH_LANG_HE = Column(JSON, nullable = True)
    # SEARCH_LANG_RU = Column(JSON, nullable = True)
    # SEARCH_LANG_EN = Column(JSON, nullable = True)


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TEST & DEBUG PROPERTIES
    
    """

    
    @property
    def STATUS_SAVED(self) -> bool:
        import random
        return random.choice((True, False))

    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PAGE LINK METHODS AND PROPERTIES
    
    """
    
    
    def __generate_page_url(self, local_language: str = "ru") -> str:
        """
        Generates a Pealim dictionary URL for the word in the specified language.
        
        Constructs a URL pointing to the word's dictionary entry on pealim.com
        in the requested language interface. The word is identified by its index
        and the interface language is determined by the language tag.
        
        ## Examples:
            >>> self.__generate_page_url(local_language = "ru")
            'https://www.pealim.com/ru/dict/17'
            >>> self.__generate_page_url(local_language = "en")
            'https://www.pealim.com/en/dict/17'
            >>> self.__generate_page_url(local_language = "he") 
            'https://www.pealim.com/he/dict/17'
            >>> self.__generate_page_url(local_language = "Russian")
            'https://www.pealim.com/ru/dict/17'
            >>> self.__generate_page_url(local_language = "English")
            'https://www.pealim.com/en/dict/17'
        
        :param str local_language: Language specification. Can be either a two-letter language tag 
            ('en', 'ru', 'he') or full language name ('English', 'Russian', 'Hebrew'). Only the 
            first two characters are used.

        :return str: Fully qualified URL to the word's dictionary page in the 
            specified language interface.
            
        :raises ValueError: If local_language is empty or cannot be processed.
        """
        
        # Generating url to the word:
        word_index: str = str(self.INDEX)
        language_tag: str = local_language[:2].lower()
        page_url: str = f"https://www.pealim.com/{language_tag}/dict/{word_index}"
        
        # Returning:
        return page_url
    
    
    @property
    def PEALIM_URL_RU(self) -> str:
        """
        Russian interface URL for the word on Pealim dictionary.
        
        Provides direct access to the word's dictionary entry with Russian interface localization. 
        This is a convenience property that returns the same result as calling private method 
        `__generate_page_url("ru")`.
        
        :return str: URL to the word's dictionary page with Russian interface.
        """
        
        # Aquiring url in local language:
        page_url: str = self.__generate_page_url(local_language = "ru")
        
        # Returning:
        return page_url
    

    @property
    def PEALIM_URL_EN(self) -> str:
        """
        English interface URL for the word on Pealim dictionary.
        
        Provides direct access to the word's dictionary entry with English interface localization. 
        This is a convenience property that returns the same result as calling 
        `__generate_page_url("en")`.
        
        :return str: URL to the word's dictionary page with English interface.
        """
        
        # Aquiring url in local language:
        page_url: str = self.__generate_page_url(local_language = "en")
        
        # Returning:
        return page_url


    @property
    def PEALIM_URL_HE(self) -> str:
        """
        Hebrew interface URL for the word on Pealim dictionary.
        
        Provides direct access to the word's dictionary entry with Hebrew interface localization. 
        This is a convenience property that returns the same result as calling 
        `__generate_page_url("he")`.
        
        :return str: URL to the word's dictionary page with Hebrew interface.
        """
        
        # Aquiring url in local language:
        page_url: str = self.__generate_page_url(local_language = "he")
        
        # Returning:
        return page_url
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    COMPOSITION METHODS
    
    """


    def __compose_translation(self) -> None:
        """
        TODO: Create a docstring.
        """

        ...

    
    def __compose_transcribtion(self) -> None:
        """
        TODO: Create a docstring.
        """

        ...
        
        
    def __repair(self) -> None:
        """
        Cleans and rewrites internal links in all language HTML containers.

        Rules:
        - Keeps only links of type `/dict/<id>-...` and converts them to `/dictionary/<lang>/<id>`
        - Removes or unlinks all links containing `/dict/?...`
        - Updates each HTML_CONTAINER_LANG_<lang> field in place
        """

        # Composing language to container index dictionary:        
        locale_html_index = {
            "ru": self.HTML_CONTAINER_LANG_RU,
            "en": self.HTML_CONTAINER_LANG_EN,
            "he": self.HTML_CONTAINER_LANG_HE,
            }

        # Looping through all languages and their containers:
        for language, container_html in locale_html_index.items():
            if not container_html:
                continue

            # Creating soup instance:
            soup = BeautifulSoup(container_html, "html.parser")
            
            # Searching for all anchor tags:            
            html_changed = False
            for tag_a in soup.find_all("a", href=True):
                href_attribute = tag_a["href"]

                # Removing radical/parameter links:
                link_remove_pattern: str = r"/dict/\?.+"
                link_remove_found = re.search(link_remove_pattern, href_attribute)
                if link_remove_found:
                    tag_a.unwrap()
                    html_changed = True
                    continue

                # Matching dict/<id> pattern (with optional slug)
                link_match_pattern: str = r"/dict/(\d+)(?:-[\w-]*)?/?"
                link_match_found = re.search(link_match_pattern, href_attribute)
                if link_match_found:
                    word_id = link_match_found.group(1)
                    href_attribute_replace = f"/dictionary/{language}/{word_id}"
                    tag_a["href"] = href_attribute_replace
                    html_changed = True

            # Converting soup back to HTML string:
            if html_changed:
                updated_html = str(soup)
                
                # Updating attribute:
                if language == "ru":
                    self.HTML_CONTAINER_LANG_RU = updated_html
                elif language == "en":
                    self.HTML_CONTAINER_LANG_EN = updated_html
                elif language == "he":
                    self.HTML_CONTAINER_LANG_HE = updated_html

    
    def compose(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Reparing HTML containers:
        self.__repair()

    