# Default logger import:
import logging
log = logging.getLogger(__name__)

# Database types:
from sqlalchemy import Column, Integer, String, JSON, Boolean

# Database import:
from utilities.database import DATABASE


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
WORD DATABASE MODEL

"""


class Input(DATABASE.Model):
    """
    TODO: Create a docstring.
    """
    
    
    # Assigning table name:
    __tablename__: str = "inputs"
    
    # Core attributes:
    ID = Column(Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    
    # Word attributes:
    WORD_HE = Column(String, nullable = True)
    STEM_HE = Column(String, nullable = True)
    TRANSCRIPTION_RU = Column(String, nullable = True)
    TRANSLATION_RU = Column(String, nullable = True)
    POS_RU = Column(String, nullable = True)
    INF_RU = Column(String, nullable = True)

    