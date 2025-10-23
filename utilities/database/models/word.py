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
    
    # Translation and transcribtion attributes:
    TRANSLATION_LANG_HE = Column(String, nullable = True)
    TRANSLATION_LANG_RU = Column(String, nullable = True)
    TRANSLATION_LANG_EN = Column(String, nullable = True)
    TRANSCRIPTION_LANG_HE = Column(String, nullable = True)
    TRANSCRIPTION_LANG_RU = Column(String, nullable = True)
    TRANSCRIPTION_LANG_EN = Column(String, nullable = True)
    TYPE_LANG_HE = Column(String, nullable = True)
    TYPE_LANG_RU = Column(String, nullable = True)
    TYPE_LANG_EN = Column(String, nullable = True)
    SEARCH_LANG_HE = Column(JSON, nullable = True)
    SEARCH_LANG_RU = Column(JSON, nullable = True)
    SEARCH_LANG_EN = Column(JSON, nullable = True)

    # Status attributes:
    STATUS_FAVOURITE = Column(Boolean, nullable = True, default = False)
    STATUS_TO_LEARN = Column(Boolean, nullable = True, default = False)
    STATUS_KNOWN = Column(Boolean, nullable = True, default = False)


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    TEST & DEBUG PROPERTIES
    
    """

    
    ...     # <- There is nothing here yet.
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PAGE LINK METHODS AND PROPERTIES
    
    """
    
    
    def __generate_pealim_page_url(self, local_language: str = "ru") -> str:
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
        page_url: str = self.__generate_pealim_page_url(local_language = "ru")
        
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
        page_url: str = self.__generate_pealim_page_url(local_language = "en")
        
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
        page_url: str = self.__generate_pealim_page_url(local_language = "he")
        
        # Returning:
        return page_url
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    LANGUAGE LOCALE AVAILABILITY PROPERTIES
    
    """
    
    
    @property
    def LANG_RU_AVAILABLE(self) -> bool:
        """
        TODO: Create a docstring.
        """
        
        # Getting container sizes:
        container_en_size: int = len(self.HTML_CONTAINER_LANG_EN)
        container_ru_size: int = len(self.HTML_CONTAINER_LANG_RU)
        
        # Comparing container sizes:
        language_available: bool = True
        if container_en_size == container_ru_size:
            language_available: bool = False
            
        # Returning:
        return language_available
    
    
    @property
    def LANG_EN_AVAILABLE(self) -> bool:
        """
        TODO: Create a docstring.
        """
        
        # Returning:
        return True
    
    
    @property
    def LANG_HE_AVAILABLE(self) -> bool:
        """
        TODO: Create a docstring.
        """
        
        # Returning:
        return True
    
    
    
        
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    COMPOSITION METHODS
    
    """


    def __compose_translation(self, language: str) -> Optional[str]:
        """
        TODO: Create a docstring.
        """

        # Normalizing and validating language argument:
        language = language.lower().strip()

        # English and Russian extraction:
        if language in ("en", "ru"):

            # Selecting corresponding HTML container:
            html_container: Optional[str] = None
            if language == "en": html_container = self.HTML_CONTAINER_LANG_EN
            elif language == "ru": html_container = self.HTML_CONTAINER_LANG_RU

            # Returning None, if failed to select container:
            if not html_container:
                return None

            # Attempting to extract translation text:
            try:
                soup = BeautifulSoup(html_container, "html.parser")
                lead_div = soup.find("div", class_="lead")
                if not lead_div or not lead_div.text:
                    return None
                
                # Cleaning up and normalizing text
                translation_text = lead_div.get_text(strip=True)
                return translation_text or None

            # Handling exception errors and logging:
            except Exception as exception_error:
                log.warning(f"Failed to extract translation ({language}) for Word ID={self.ID}: {exception_error}")

            # Returning None if extraction fails:
            return None
        
        # Hebrew language extraction:
        elif language == "he":

            # Returning None, if failed to select container:
            html_container = self.HTML_CONTAINER_LANG_HE
            if not html_container:
                return None

            # Attempting to soup it out:
            try:
                soup = BeautifulSoup(html_container, "html.parser")
                header = soup.find("h2", class_="page-header")
                if not header or not header.text:
                    return None

                # Removing nested <span> elements:
                for span in header.find_all("span"):
                    span.decompose()

                # Formatting extracted text:
                header_text = header.get_text(
                    strip = True
                    )

                # Splitting by spaces and taking the last word:
                words = header_text.split()
                if words:
                    return words[-1]

            # Handling exceptions, logging and returning None:
            except Exception as exception_error:
                log.warning(f"Failed to extract Hebrew word for Word ID={self.ID}: {exception_error}")
                return None
        
        # Unsupported language error:
        else:
            log.warning(f"Unsupported language '{language}' for translation extraction.")
            return None
        

    def __compose_search(self, translation_text: Optional[str]) -> Optional[list[str]]:
        """
        Splits a translation string into a list of individual searchable terms.

        This method prepares language-specific search index lists by splitting the provided 
        translation string (e.g. "write, to write, compose") into a clean list of words 
        (["write", "to write", "compose"]). Empty or  whitespace-only entries are ignored.

        :param Optional[str] translation_text: The translation string to process.
        :return Optional[list[str]]: List of cleaned search terms, or None if input is empty.
        """

        # Preparing search container:
        search_container: list[str] | None= None

        # Safely split translation strings into word lists for search indexing
        if translation_text:
            search_container: list[str] = [
                token.strip() for token 
                in translation_text.split(",") 
                if token.strip()
                ]
        
        # Returning:
        return search_container
    

    def __compose_transcription(self, html_container: Optional[str]) -> Optional[str]:
        """
        Extracts the word transcription (phonetic pronunciation) from a HTML container.

        Depending on the part of speech, Pealim pages place transcriptions in different sections:
        - Verbs:      inside `<div id="INF-L">` ... `<div class="transcription">...</div>`
        - Nouns:      inside `<div id="s">` ... `<div class="transcription">...</div>`
        - Adjectives: inside `<div id="ms-a">` ... `<div class="transcription">...</div>`
        - Adverbs / Conjunctions / Others: inside `<div class="lead">` ... `<div class="transcription">...</div>`

        :return Optional[str]: Cleaned transcription text, or None if not found.
        """

        if not html_container:
            return None

        try:
            soup = BeautifulSoup(html_container, "html.parser")

            # Define possible transcription locations (order matters)
            search_selector_list = [
                ("div", {"id":    "INF-L"}),   # verbs
                ("div", {"id":    "s"}),       # nouns
                ("div", {"id":    "ms-a"}),    # adjectives
                ("div", {"class": "lead"})  # adverbs, conjunctions
                ]

            # Locating section:
            for html_tag, tag_attribute_list in search_selector_list:
                section = soup.find(
                    html_tag, 
                    attrs = tag_attribute_list
                    )
                if not section:
                    continue
                
                # Locating transcription div:
                transcription = section.find("div", class_="transcription")
                if transcription and transcription.text:

                    # Extracting text with <b> elements flattened:
                    transcription_text = transcription.get_text(strip = True)
                    return transcription_text

        # Handling exception errors and logging:
        except Exception as exception_error:
            log.warning(f"Failed to extract transcription for Word ID={self.ID}: {exception_error}")

        # Returning none, if failed to compose:
        return None

    
    def __compose_type(self, html_container: str) -> Optional[str]:

        # Returning None, if HTML container does not exist:
        if not html_container:
            return None

        # Attempting to extract an element:
        try:
            soup = BeautifulSoup(html_container, "html.parser")

            # Find the first <p> tag inside the .container div
            container = soup.find("div", class_="container")
            if not container:
                return None
            
            type_tag = container.find("p")
            if not type_tag:
                return None
            
            # Extract the text from the <p> tag and formatting:
            type_text = type_tag.get_text(strip=True)
            type_text_split = type_text.split("-")[0].strip()
            type_text_split = type_text_split.lower()
            type_text_split = type_text_split.capitalize()

            # Only return valid POS types
            return type_text_split

        # Handling exception errors and logging:
        except Exception as exception_error:
            log.warning(f"Failed to extract part of speech for Word ID={self.ID}: {exception_error}")

        # Returning none, if failed to compose:
        return None

    
    def compose(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Composing translations:
        self.TRANSLATION_LANG_HE: str = self.__compose_translation(
            language = "he"
            )
        self.TRANSLATION_LANG_EN: str = self.__compose_translation(
            language = "en"
            )
        self.TRANSLATION_LANG_RU: str = self.__compose_translation(
            language = "ru"
            )

        # Splitting translation text and composing search index lists:
        self.SEARCH_LANG_HE: Optional[list[str]] = self.__compose_search(
            translation_text = self.TRANSLATION_LANG_HE
            )
        self.SEARCH_LANG_EN: Optional[list[str]] = self.__compose_search(
            translation_text = self.TRANSLATION_LANG_EN
            )
        self.SEARCH_LANG_RU: Optional[list[str]] = self.__compose_search(
            translation_text = self.TRANSLATION_LANG_RU
            )
        
        # Finding transcription elements and extracting text:
        self.TRANSCRIPTION_LANG_HE: str = self.__compose_transcription(
            html_container = self.HTML_CONTAINER_LANG_HE
            )
        self.TRANSCRIPTION_LANG_EN: str = self.__compose_transcription(
            html_container = self.HTML_CONTAINER_LANG_EN
            )
        self.TRANSCRIPTION_LANG_RU: str = self.__compose_transcription(
            html_container = self.HTML_CONTAINER_LANG_RU
            )

        # Finding type elements and extracting text:
        self.TYPE_LANG_HE: str = self.__compose_type(
            html_container = self.HTML_CONTAINER_LANG_HE
            )
        self.TYPE_LANG_EN: str = self.__compose_type(
            html_container = self.HTML_CONTAINER_LANG_EN
            )
        self.TYPE_LANG_RU: str = self.__compose_type(
            html_container = self.HTML_CONTAINER_LANG_RU
            )
        
