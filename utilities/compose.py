# Default logger import:
import logging
log = logging.getLogger(__name__)

# Parse-related libraries import:
from bs4 import BeautifulSoup
import json

# Typing and annotations:
from typing import Dict, List

# Local settings import:
from configuration import SETTINGS

# Database-related import:
from utilities.database import DATABASE
from utilities.database.models.word import Word


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
COMPOSE LOGIC FUNCTIONS

"""

import json
from typing import Dict, List, Optional
from bs4 import BeautifulSoup


class JSONToWordModelConverter:
    """Converts JSON dictionary data to Word model instances"""
    
    def __init__(self, json_filepath: str):
        self.json_filepath = json_filepath
        self.data = self._load_json_data()
    
    def _load_json_data(self) -> Dict:
        """Load JSON data from file"""
        try:
            with open(self.json_filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON: {e}")
            return {}
    
    def extract_hebrew_word(self, container_html: str) -> Optional[str]:
        """
        Extract Hebrew word from <h2 class='page-header'> element.
        Finds the first token in the header text that contains Hebrew characters.
        """
        import re 
        
        if not container_html:
            print("❌ No container HTML provided")
            return None

        try:
            soup = BeautifulSoup(container_html, 'html.parser')
            page_header = soup.find('h2', class_='page-header')

            if not page_header:
                print("❌ No h2.page-header found")
                return None

            header_text = page_header.get_text().strip()
            print(f"🔍 Header text: '{header_text}'")

            words = header_text.split()
            print(f"🔍 Split words: {words}")

            # Find the first word containing Hebrew characters
            hebrew_word = next((w for w in words if re.search(r'[\u0590-\u05FF]', w)), None)
            print(f"🔍 Extracted word: '{hebrew_word}'")

            if hebrew_word:
                print("✅ Hebrew characters detected")
                return hebrew_word
            else:
                print("❌ No Hebrew characters found in header text")
                return None

        except Exception as e:
            print(f"❌ Error extracting Hebrew word: {e}")
            return None

    
    
    def extract_translation_from_lead(self, lead_html: str) -> Optional[str]:
        """Extract translation text from lead div"""
        if not lead_html:
            return None
            
        try:
            soup = BeautifulSoup(lead_html, 'html.parser')
            lead_div = soup.find('div', class_='lead')
            return lead_div.get_text(strip=True) if lead_div else None
        except Exception as e:
            print(f"Error extracting translation: {e}")
            return None
    
    
    def json_entry_to_word_model(self, page_index: str, entry_data: Dict) -> Optional[Word]:
        """
        Convert a single JSON entry to a Word model instance
        
        Args:
            page_index: The page index (JSON key)
            entry_data: The dictionary containing language data
            
        Returns:
            Word model instance or None if conversion fails
        """
        try:
            # Extract HTML containers
            ru_container = entry_data.get('ru', {}).get('container', '')
            en_container = entry_data.get('en', {}).get('container', '')
            he_container = entry_data.get('he', {}).get('container', '')
            
            # Extract translations
            ru_translation = self.extract_translation_from_lead(
                entry_data.get('ru', {}).get('lead', '')
            )
            en_translation = self.extract_translation_from_lead(
                entry_data.get('en', {}).get('lead', '')
            )
            he_translation = self.extract_hebrew_word(en_container)
            
            # Create Word instance
            word_instance = Word(
                INDEX=int(page_index),
                HTML_CONTAINER_LANG_RU=ru_container,
                HTML_CONTAINER_LANG_EN=en_container,
                HTML_CONTAINER_LANG_HE=he_container,
                TRANSLATION_LANG_RU=ru_translation,
                TRANSLATION_LANG_EN=en_translation,
                TRANSLATION_LANG_HE=he_translation,
                TRANSCRIBTION_LANG_RU=None,  # Will be populated later
                TRANSCRIBTION_LANG_EN=None   # Will be populated later
            )
            
            return word_instance
            
        except Exception as e:
            print(f"Error converting page {page_index} to model: {e}")
            return None
    
    
    def convert_all_entries(self) -> List[Word]:
        """Convert all JSON entries to Word model instances"""
        word_instances = []
        
        for page_index, entry_data in self.data.items():
            word_instance = self.json_entry_to_word_model(page_index, entry_data)
            if word_instance:
                word_instances.append(word_instance)
        
        print(f"✅ Converted {len(word_instances)} entries to model instances")
        return word_instances
    
    
    def convert_and_save_to_db(self, batch_size: int = 100) -> int:
        """
        Convert JSON entries and save to database in batches
        
        Args:
            batch_size: Number of records to insert per batch
            
        Returns:
            Number of successfully saved records
        """
        word_instances = self.convert_all_entries()
        saved_count = 0
        
        for i in range(0, len(word_instances), batch_size):
            batch = word_instances[i:i + batch_size]
            
            try:
                DATABASE.session.bulk_save_objects(batch)
                DATABASE.session.commit()
                saved_count += len(batch)
                print(f"✅ Saved batch {i//batch_size + 1}: {len(batch)} records")
                
            except Exception as e:
                DATABASE.session.rollback()
                print(f"❌ Error saving batch {i//batch_size + 1}: {e}")
                # Try saving individually
                for word in batch:
                    try:
                        DATABASE.session.add(word)
                        DATABASE.session.commit()
                        saved_count += 1
                    except:
                        DATABASE.session.rollback()
        
        print(f"🎉 Total saved to database: {saved_count} records")
        return saved_count


# 🎯 Simple Function-Based Approach
def json_to_word_models_simple(json_filepath: str) -> List[Word]:
    """
    Simple one-shot conversion from JSON to Word models
    
    Args:
        json_filepath: Path to JSON file
        
    Returns:
        List of Word model instances
    """
    converter = JSONToWordModelConverter(json_filepath)
    return converter.convert_all_entries()


def save_words_to_db(word_instances: List[Word]) -> int:
    """
    Save Word instances to database
    
    Args:
        word_instances: List of Word model instances
        
    Returns:
        Number of successfully saved records
    """
    try:
        DATABASE.session.bulk_save_objects(word_instances)
        DATABASE.session.commit()
        print(f"✅ Saved {len(word_instances)} records to database")
        return len(word_instances)
    except Exception as e:
        DATABASE.session.rollback()
        print(f"❌ Error saving to database: {e}")
        return 0


# 🧪 Test Functions
def test_conversion(json_filepath: str, test_count: int = 3):
    """Test the conversion process with sample data"""
    converter = JSONToWordModelConverter(json_filepath)
    
    print("🧪 Testing JSON to Model Conversion")
    print("=" * 50)
    
    # Test single entry
    test_entries = list(converter.data.items())[:test_count]
    
    for page_index, entry_data in test_entries:
        print(f"\n📄 Testing page {page_index}:")
        
        # Debug: Check what languages we have
        print(f"  📊 Available languages: {list(entry_data.keys())}")
        
        # Debug: Check Hebrew container
        he_container = entry_data.get('he', {}).get('container', '')
        print(f"  📊 HE container length: {len(he_container)}")
        
        if he_container:
            # Test Hebrew extraction directly
            hebrew_word = converter.extract_hebrew_word(he_container)
            print(f"  🔍 Direct Hebrew extraction: '{hebrew_word}'")
        
        word_instance = converter.json_entry_to_word_model(page_index, entry_data)
        if word_instance:
            print(f"  ✅ INDEX: {word_instance.INDEX}")
            print(f"  ✅ RU: '{word_instance.TRANSLATION_LANG_RU}'")
            print(f"  ✅ EN: '{word_instance.TRANSLATION_LANG_EN}'")
            print(f"  ✅ HE: '{word_instance.TRANSLATION_LANG_HE}'")
            print(f"  ✅ Containers: "
                  f"RU({len(word_instance.HTML_CONTAINER_LANG_RU)}) "
                  f"EN({len(word_instance.HTML_CONTAINER_LANG_EN)}) "
                  f"HE({len(word_instance.HTML_CONTAINER_LANG_HE)})")
        else:
            print(f"  ❌ Failed to convert page {page_index}")


def quick_convert_and_save(json_filepath: str):
    """Quick one-liner to convert and save all data"""
    word_instances = json_to_word_models_simple(json_filepath)
    save_words_to_db(word_instances)


# 🚀 Main Execution
def check():
    JSON_FILE = SETTINGS.JSON_COLLECTION_FILEPATH
    
    # Test first
    test_conversion(JSON_FILE, 3)
    
    # Full conversion
    converter = JSONToWordModelConverter(JSON_FILE)
    converter.convert_and_save_to_db()
    