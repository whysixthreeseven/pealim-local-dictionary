# Default logger import:
import logging
log = logging.getLogger(__name__)

# Parse-related libraries import:
from bs4 import BeautifulSoup
import json

# Local settings import:
from configuration import SETTINGS

# Database-related import:
from utilities.database import DATABASE
from utilities.database.models.word import Word


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
COMPOSE LOGIC FUNCTIONS

"""


def compose() -> None:
    """
    TODO: Create a docstring.
    """

    ...


import json
from typing import Dict, List


class Processor:
    """
    TODO: Create a docstring.
    """
    
    def __init__(self):
        self.json_data = self.load_json_data()
    
    
    def load_json_data(self) -> Dict:
        """
        TODO: Create a docstring.
        """
        
        # Attempting to load file and extract data:
        try:
            json_collection_path: str = SETTINGS.JSON_COLLECTION_FILEPATH
            with open(file = json_collection_path, mode = 'r', encoding = 'UTF-8') as json_file:
                return json.load(json_file)
            
        # Raising error, if file cannot be opened or decoded:
        except FileNotFoundError:
            print(f"JSON file not found: {json_collection_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
    

    def extract_lead_content(self, html_content: str, language: str = "ru") -> str:
        """
        TODO: Create a docstring. Extract text content from lead div.
        """
        
        if not html_content:
            return ""
        
        if language == "he":
            if not html_content:
                return ""
                
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                page_header = soup.find('h2', class_='page-header')
                
                if not page_header:
                    return ""
                
                # Get the text content and remove any print-specific spans
                header_text = page_header.get_text()
                
                # Split by spaces and get the last element (Hebrew word)
                words = header_text.strip().split()
                if words:
                    hebrew_word = words[-1]
                    # Basic validation - check if it contains Hebrew characters
                    if any('\u0590' <= char <= '\u05FF' for char in hebrew_word):
                        return hebrew_word
                
                return ""
                
            except Exception as e:
                print(f"Error extracting Hebrew word: {e}")
                return ""

        
        else:
            
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                lead_div = soup.find('div', class_='lead')
                return lead_div.get_text(strip=True) if lead_div else ""
            except Exception as e:
                print(f"Error extracting lead content: {e}")
                return ""
    
    
    def process_entry(self, page_index: str, entry_data: Dict) -> Word:
        """
        TODO: Create a docstring.
        
        Process a single JSON entry and create a Word model instance
        """
        
        # Extracting HTML containers for each language:
        container_ru = entry_data.get('ru', {}).get('container', '')
        container_en = entry_data.get('en', {}).get('container', '')
        container_he = entry_data.get('he', {}).get('container', '')
        
        # Extracting translations from lead content:
        translation_ru = self.extract_lead_content(
            html_content = entry_data.get('ru', {}).get('lead', ''),
            language = "ru"
            )
        translation_en = self.extract_lead_content(
            html_content = entry_data.get('en', {}).get('lead', ''),
            language = "en",
            )
        translation_he = self.extract_lead_content(
            html_content = container_he,
            language = "he"
            )
        
        # Creating database Word instance object:
        word_instance = Word(
            
            # Getting index from page index:
            INDEX = int(page_index),
            
            # Populating html containers for later rendering and composing:
            HTML_CONTAINER_LANG_RU = container_ru,
            HTML_CONTAINER_LANG_EN = container_en,
            HTML_CONTAINER_LANG_HE = container_he,
            
            # Extracting word translation:
            TRANSLATION_LANG_RU = translation_ru or None,
            TRANSLATION_LANG_EN = translation_en or None,
            TRANSLATION_LANG_HE = translation_he or None,
            
            # Transcribtion fields will be populated later:
            TRANSCRIBTION_LANG_RU = None,
            TRANSCRIBTION_LANG_EN = None
            )
        
        return word_instance
    
    
    def test_single_entry(self, page_index: str = "1"):
        """Test processing a single entry"""
        if page_index not in self.json_data:
            print(f"Page index {page_index} not found in JSON data")
            return None
        
        print(f"Testing processing for page index: {page_index}")
        print("=" * 50)
        
        entry_data = self.json_data[page_index]
        word_instance = self.process_entry(page_index, entry_data)
        
        # Display results
        print(f"Created Word instance:")
        print(f"  INDEX: {word_instance.INDEX}")
        print(f"  RU Translation: {word_instance.TRANSLATION_LANG_RU}")
        print(f"  EN Translation: {word_instance.TRANSLATION_LANG_EN}")
        print(f"  HE Translation: {word_instance.TRANSLATION_LANG_HE}")
        print(f"  RU Container length: {len(word_instance.HTML_CONTAINER_LANG_RU)}")
        print(f"  EN Container length: {len(word_instance.HTML_CONTAINER_LANG_EN)}")
        print(f"  HE Container length: {len(word_instance.HTML_CONTAINER_LANG_HE)}")
        
        return word_instance
    
    
    def test_multiple_entries(self, count: int = 5):
        """Test processing multiple entries"""
        print(f"Testing first {count} entries:")
        print("=" * 50)
        
        processed_count = 0
        word_instances = []
        
        for page_index, entry_data in list(self.json_data.items())[:count]:
            print(f"\nProcessing page {page_index}:")
            
            word_instance = self.process_entry(page_index, entry_data)
            word_instances.append(word_instance)
            
            print(f"  ✓ Translation: {word_instance.TRANSLATION_LANG_RU} | {word_instance.TRANSLATION_LANG_EN}")
            print(f"  ✓ Containers: RU({len(word_instance.HTML_CONTAINER_LANG_RU)}) EN({len(word_instance.HTML_CONTAINER_LANG_EN)}) HE({len(word_instance.HTML_CONTAINER_LANG_HE)})")
            
            processed_count += 1
        
        print(f"\n✅ Successfully processed {processed_count} entries")
        return word_instances
    
    
    def validate_data_quality(self, sample_size: int = 10):
        """Validate the quality of extracted data"""
        print("Data Quality Validation:")
        print("=" * 50)
        
        issues = []
        valid_entries = 0
        
        for page_index, entry_data in list(self.json_data.items())[:sample_size]:
            # Check if all languages have containers
            has_ru = bool(entry_data.get('ru', {}).get('container'))
            has_en = bool(entry_data.get('en', {}).get('container'))
            has_he = bool(entry_data.get('he', {}).get('container'))
            
            # Check if translations are extracted
            ru_trans = self.extract_lead_content(entry_data.get('ru', {}).get('lead', ''))
            en_trans = self.extract_lead_content(entry_data.get('en', {}).get('lead', ''))
            he_trans = self.extract_lead_content(entry_data.get('he', {}).get('lead', ''))
            
            if not all([has_ru, has_en, has_he]):
                issues.append(f"Page {page_index}: Missing containers (RU:{has_ru}, EN:{has_en}, HE:{has_he})")
            
            if not any([ru_trans, en_trans, he_trans]):
                issues.append(f"Page {page_index}: No translations extracted")
            else:
                valid_entries += 1
        
        print(f"Valid entries: {valid_entries}/{sample_size}")
        print(f"Issues found: {len(issues)}")
        
        for issue in issues[:5]:  # Show first 5 issues
            print(f"  ⚠️ {issue}")
        
        return valid_entries, issues


def main():
    """Main test function"""
    # Initialize processor
    processor = Processor()
    
    print("JSON to Model Conversion Test")
    print("=" * 60)
    
    # Check if data is loaded
    if not processor.json_data:
        print("❌ No data loaded. Check JSON file path.")
        return
    
    print(f"✅ Loaded {len(processor.json_data)} entries from JSON")
    
    # Test single entry
    print("\n1. Testing single entry processing:")
    word_instance = processor.test_single_entry("1")
    
    # Test multiple entries
    print("\n2. Testing multiple entries processing:")
    word_instances = processor.test_multiple_entries(5)
    
    # Validate data quality
    print("\n3. Data quality validation:")
    processor.validate_data_quality(10)
    
    # Test database insertion (optional)
    print("\n4. Testing database insertion:")
    try:
        # Add to database session (but don't commit for test)
        if word_instance:
            DATABASE.session.add(word_instance)
            print("✅ Word instance ready for database insertion")
            # DATABASE.session.commit()  # Uncomment to actually save
        else:
            print("❌ No word instance to insert")
    except Exception as e:
        print(f"❌ Database error: {e}")


if __name__ == "__main__":
    main()
