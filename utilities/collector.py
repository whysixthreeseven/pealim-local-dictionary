# Default logger import:
import logging
log = logging.getLogger(__name__)

# Core script library imports:
import aiohttp
import asyncio
import json

# Beautiful soup import:
from bs4 import BeautifulSoup

# Typing, annotations and time:
from typing import Dict, List, Optional
import time

# Local settings import:
from configuration import SETTINGS


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
SCARPPER CLASS INSTANCE BLOCK

"""


class MultiLanguageScraper:

    
    def __init__(self, page_count_max: int, batch_size: int):
        
        # Task attributes:
        self.paelim_page_count: int = page_count_max
        self.paelim_page_batch: int = batch_size
        
        # Results dictionary:
        self.results: dict[str, dict[str, str]] = {}
        
        # URL and locale attributes:
        self.paelim_url = "https://www.pealim.com/{lang}/dict/{page_id}"
        self.locale_list: tuple[str, ...] = ("ru", "en", "he")
        
        
    async def fetch_page(self, 
                         session: aiohttp.ClientSession,    # <- Session instance
                         locale: str,                       # <- Locale variable (e.g. "en", "ru", or "he")
                         page_index: int                    # <- Page index, as is on the website
                         ) -> Optional[Dict]:
        """
        TODO: Create a docstring.
        """
        
        # Generating page URL (from instance attribute)
        page_url = self.paelim_url.format(
            lang = locale, 
            page_id = page_index
            )
        
        # Aquiring page and parsing:
        try:
            conf_timeout = aiohttp.ClientTimeout(total = 30)
            async with session.get(url = page_url, timeout = conf_timeout) as response:
                
                # Asserting connection:
                if response.status != 200:
                    return None
                    
                # Acquiring page document:
                html_document: str = await response.text()
                
                # Asserting dictionary instance exists (internally):
                if 'class="not-found"' in html_document:
                    return None
                
                # Parsing document with soup extension:
                soup = BeautifulSoup(html_document, 'html.parser')
                lead_div = soup.find('div', class_='lead')
                lead_content = str(lead_div) if lead_div else None
                container_div = soup.find('div', class_='container')
                container_content = str(container_div) if container_div else None
                
                # Returning data, if found both:
                if lead_content and container_content:
                    page_content: dict[str, str] = {"lead": lead_content, "container": container_content}
                    return page_content
                else:
                    return None
                    
        except Exception as e:
            print(f"Error fetching {page_url}: {e}")
            return None
    
    
    async def verify_page(self, 
                          client_session: aiohttp.ClientSession, 
                          page_index: int) -> bool:
        
        # Cycling through available locales:
        for lang in self.locale_list:
            
            # Generating and connecting to page url:
            page_url = self.paelim_url.format(
                lang = lang, 
                page_id = page_index
                )
            try:
                async with client_session.get(page_url, timeout = aiohttp.ClientTimeout(total = 10)) as response:
                    if response.status == 200:
                        html_document = await response.text()
                        if 'class="not-found"' not in html_document:
                            return True
            
            # Continue to next language, if not found:
            except:
                continue
            
        # If none found, returning:
        return False
    
    
    async def scrape_page(self, client_session: aiohttp.ClientSession, page_index: int) -> Optional[Dict]:
        """
        Scraping page:
        """
        
        # Asserting page entry exists:
        if not await self.verify_page(
            client_session = client_session, 
            page_index = page_index
            ):
            return None
        
        # Results variables:
        page_data: dict[str, str] = {}      # <- "language": {"lead": "...", "container": "..."}
        page_valid: bool = False
        
        # Cycling through locales:
        for language in self.locale_list:
            language_data = await self.fetch_page(client_session, language, page_index)
            if language_data:
                page_data[language] = language_data
                page_valid = True
        
        # Getting return container
        data_container = None
        if page_valid:
            data_container = {page_index: page_data}
            
        # Returning:
        return data_container
    
    
    async def process_batch(self, session: aiohttp.ClientSession, batch: List[int]) -> Dict:
        """
        Process a batch of page indexes
        """
        
        batch_results = {}
        
        tasks = [self.scrape_page(session, page_id) for page_id in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                print(f"Exception in batch processing: {result}")
                continue
                
            if result is not None:
                batch_results.update(result)
        
        return batch_results
    
    
    async def run(self):
        """
        TODO: Create a docstring.
        """
        
        # Configuring client session:
        conf_connector = aiohttp.TCPConnector(
            limit = 50, 
            limit_per_host = 10
            )
        conf_timeout = aiohttp.ClientTimeout(
            total = 30
            )
        conf_headers: dict[str, str] = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'} 
        
        async with aiohttp.ClientSession(
            connector = conf_connector,
            timeout = conf_timeout,
            headers = conf_headers
            ) as session:
            
            # Filtering out pages that are already in results
            page_index_all = list(range(1, self.paelim_page_count + 1))
            page_index_remaining: list[int] = [
                page_index for page_index
                in page_index_all
                if str(page_index) not in self.results
                ]
            paelim_page_range: range = range(0, len(page_index_remaining), self.paelim_page_batch)      # Start, Stop, Step
        
            # Processing task pages:
            for index in paelim_page_range:
                batch_index = page_index_remaining[index:index + self.paelim_page_batch]
                batch_number = index//self.paelim_page_batch + 1
                total_batches = len(paelim_page_range)
                print(f"\nProcessing batch {batch_number}/{total_batches}: pages {batch_index[0]}-{batch_index[-1]}")
                
                # Starting task on batch:
                start_time = time.time()
                batch_results = await self.process_batch(session, batch_index)
                elapsed_time = time.time() - start_time
                
                # Updating results:
                self.results.update(batch_results)
                print(f"Batch completed in {elapsed_time:.2f}s. Found {len(batch_results)} valid pages. Total so far: {len(self.results)}")
                
                # Saving progress after each batch task:
                self.save_progress()
    
    
    def save_progress(self):
        """
        Saves current progress to JSON file.
        """
        
        # Opening and saving results to JSON file:
        json_filepath: str = SETTINGS.JSON_COLLECTION_FILEPATH
        with open(file = json_filepath, mode = 'w', encoding = 'UTF-8') as json_file:
            json.dump(
                obj = self.results, 
                fp = json_file, 
                indent = 2, 
                ensure_ascii = False
                )
        print(f"Progress saved to {json_filepath}")
    
    
    def load_progress(self):
        """
        Loads existing progress from JSON file.
        """
        
        # Attempting locate and load existing JSON file:
        try:
            json_filepath: str = SETTINGS.JSON_COLLECTION_FILEPATH
            with open(file = json_filepath, mode = 'r', encoding = 'UTF-8') as json_file:
                self.results = json.load(
                    fp = json_file
                    )
            log.info(f"Loaded {len(self.results)} existing entries..")
        
        # Raising error, if no file found:
        except FileNotFoundError:
            log.info("No existing progress file found. Starting fresh...")


"""
###################################################################################################
SCRIPT ENTRY POINT

"""


async def __collect_dictionary():
    """
    TODO: Create a docstring.
    """
    
    # Default task values:
    PAELIM_PAGE_MAX: int = 10000
    PAELIM_PAGE_BATCH: int = 100
    
    # Calling Scrapper and continuing (if task exists)
    log.info(f"Scrapper instance initialized with {PAELIM_PAGE_MAX=} & {PAELIM_PAGE_BATCH=}")
    scraper = MultiLanguageScraper(
        page_count_max = PAELIM_PAGE_MAX, 
        batch_size = PAELIM_PAGE_BATCH
        )
    scraper.load_progress()
    
    # Running the scrapper:
    await scraper.run()
    
    # Finalizing and saving JSON file:
    scraper.save_progress()
    log.info(f"Scraping completed. Found f{len(scraper.results)} valid pages!")
    

def collect_dictionary():
    asyncio.run(__collect_dictionary())

