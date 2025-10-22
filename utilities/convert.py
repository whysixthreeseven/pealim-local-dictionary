# Default logger import:
import logging
log = logging.getLogger(__name__)

# Parse-related libraries import:
import json

# Typing and annotations:
from typing import Dict, List, Optional

# Threaded composition library:
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Local settings import:
from configuration import SETTINGS

# Database-related import:
from utilities.database import DATABASE
from utilities.database.models.word import Word


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CONVERTER CLASS INSTANCE

"""


class Converter:
    """
    Converts JSON dictionary data to Word model instances for database storage.
    
    This class handles the transformation of scraped dictionary data from JSON format into 
    SQLAlchemy Word model instances, with support for batch processing and database insertion.
    
    Attributes:
        json_filepath (str): Path to the JSON file containing scraped dictionary data
        json_data (Dict): Loaded JSON data as Python dictionary
    """
    
    def __init__(self, json_filepath: str):
        """
        Initialize the Converter with a JSON data source.
        
        :param str json_filepath: Path to the JSON file containing scraped Pealim dictionary data
            in the format `{page_index: {language: {lead: ..., container: ...}}}`
        """

        # Core attributes:
        self.json_filepath: str = json_filepath
        self.json_data: Dict = self.__load_data()
    

    def __load_data(self) -> Dict:
        """
        Load JSON data from the specified file path.
        
        :return Dict: Dictionary containing the parsed JSON data, or empty dict if file not found.
            or invalid JSON.
            
        :raise FileNotFoundError: If the JSON file does not exist (handled internally);
        :raise JSONDecodeError: If the file contains invalid JSON (handled internally).
        """

        # Attempting to load JSON data:
        try:
            with open(file = self.json_filepath, mode = 'r', encoding = 'UTF-8') as json_file:
                return json.load(json_file)
            
        # Raising error on failed loading:
        except (FileNotFoundError, json.JSONDecodeError) as exception_error:
            log.error(f"Error loading JSON: {exception_error}")
            return {}
    
    
    def __extract(self, page_index: str, entry_data: Dict) -> Optional[Word]:
        """
        Convert a single JSON entry to a Word model instance.
        
        Extracts the HTML containers for each language (Russian, English, Hebrew) and creates a 
        Word model instance with the basic structure. Additional processing like translation 
        extraction should be handled separately.
        
        :param str page_index: The page index from JSON keys (e.g., `"1"`, `"2"`, `"3"` etc.);
        :param Dict entry_data: Dictionary containing language data in format: 
            `{'ru': {'container': ...}, 'en': {'container': ...}, 'he': {'container': ...}}`.
            
        :return Word: Word model instance with HTML containers populated, or None if conversion 
            fails.
            
        """

        # Extracting page index and HTML containers
        try:
            page_index: int = int(page_index)
            container_ru = entry_data.get('ru', {}).get('container', '')
            container_en = entry_data.get('en', {}).get('container', '')
            container_he = entry_data.get('he', {}).get('container', '')
                        
            # Create Word instance
            word_instance = Word(
                INDEX = int(page_index),
                HTML_CONTAINER_LANG_RU = container_ru,
                HTML_CONTAINER_LANG_EN = container_en,
                HTML_CONTAINER_LANG_HE = container_he,
                )
            
            # Returning:
            return word_instance
            
        # Raising error on failed conversion:
        except Exception as exception_error:
            log.error(f"Error converting page {page_index} to model: {exception_error}")
            return None
        
    
    def __compose(self, word_instance: Word) -> None:
        """
        TODO: Create a docstring.
        """

        # Running compose method on word instance:
        word_instance.compose()
    
    
    def __convert(self) -> List[Word]:
        """
        Convert all JSON entries to Word model instances.
        
        Processes each entry in the loaded JSON data through the extract() method and collects all 
        successfully converted Word instances. This method only creates basic Word instances with 
        HTML containers. Additional processing may be required to extract translations and prepare 
        search attributes.
        
        :return List: List of Word model instances ready for database insertion.
        """
        
        # Logging:
        log.info(f"Converting extracted JSON data to model instances and composing data...")

        # Extracting data and creating Word instance:
        word_entry_list: list[Word] = []
        for page_index, entry_data in self.json_data.items():
            word_instance = self.__extract(
                page_index = page_index, 
                entry_data = entry_data
                )
            
            # If successful, adding to the list:
            if word_instance:
                word_entry_list.append(
                    word_instance
                    )
        
        # Running compose() concurrently on threads:
        max_workers: int = min(32, (os.cpu_count() or 1) * 2)     # <- For better machines
        # max_workers: int = 4                                      # <- For my old potato
        with ThreadPoolExecutor(max_workers = max_workers) as executor:
            futures = [executor.submit(self.__compose, word_instance) for word_instance in word_entry_list]
            for future in as_completed(futures):
                try:
                    future.result()

                # Logging error:
                except Exception as exception_error:
                    log.error(f"Error composing word: {exception_error}")
        
        # Logging:
        word_entry_count: int = len(word_entry_list)
        log.info(f"Converted {word_entry_count} entries to model instances")
        
        # Returning:
        return word_entry_list
    
    
    def run(self, entry_batch_size: int = 100) -> int:
        """
        Convert JSON entries and save to database in batches.
        
        This is the main execution method that performs the complete conversion pipeline: loading 
        JSON data, converting to model instances, and saving to the database with batch processing 
        for efficiency and error recovery. If a batch fails, individual record insertion is 
        attempted as a fallback to maximize data preservation.
        
        :param int entry_batch_size: Number of records to insert per batch. Smaller batches use 
        less memory but take longer, larger batches are faster but may encounter memory issues.
                            
        :return int: Number of successfully saved records to database.
        """
        
        # Converting JSON to models:
        word_entry_list: List[Word] = self.__convert()
        word_entry_saved_count: int = 0
        
        # Looping through all the Word model entries:
        for index in range(0, len(word_entry_list), entry_batch_size):
            entry_batch = word_entry_list[index:index + entry_batch_size]
            
            # Attempting to commit list of entries:
            batch_count: int = len(entry_batch)
            batch_index: int = index // entry_batch_size + 1
            try:
                DATABASE.session.bulk_save_objects(entry_batch)
                DATABASE.session.commit()

                # Echo:
                word_entry_saved_count += batch_count
                print(f"Saved batch {batch_index}: {batch_count} records")
            
            # Rolling back in case of an error:
            except Exception as exception_error:
                DATABASE.session.rollback()
                print(f"Error saving batch {batch_index}: {exception_error}")

                # Attempting to commit entries individually:
                print("Attempting to save entries manually...")
                for entry in entry_batch:
                    try:
                        DATABASE.session.add(entry)
                        DATABASE.session.commit()
                        word_entry_saved_count += 1
                    
                    # Rolling back in case of an error:
                    except:
                        DATABASE.session.rollback()
        
        # Logging:
        log.info(f"Entries total saved to database: {word_entry_saved_count} records")

        # Returning:
        return word_entry_saved_count


def run():
    """
    Execute the complete JSON-to-database conversion pipeline.
    
    This is the main entry point for converting scraped Pealim dictionary data from JSON format 
    to database records. It initializes the Converter with the configured JSON file path and 
    executes the conversion process.
    
    ## Workflow
    1. Loading JSON data from settings-specified path;
    2. Converting to Word model instances;
    3. Saving to database with batch processing;
    4. Logging results and errors.
    
    ## Usage
    Call this function to populate the database with dictionary data
    after scraping is complete.
    """

    # Initializing full JSON conversion:
    converter = Converter(
        json_filepath = SETTINGS.JSON_COLLECTION_FILEPATH
        )
    converter.run()
    
