# Default logger import:
import logging
log = logging.getLogger(__name__)


class Session:
    """
    TODO: Create a docstring.
    """

    # Verification variables:
    JSON_DATA_ATTACHED: bool = False
    JSON_DATA_COUNT: int = 0
    DATABASE_ATTACHED: bool = False
    DATABASE_ENTRY_COUNT: int = 0


    def verify_data(self) -> None:
        from utilities import verification

        # Logging:
        log.info("Starting data verification process...")

        JSON_DATA_EXISTS: bool = verification.verify_json_data_attached()
        if JSON_DATA_EXISTS: 
            JSON_DATA_COUNT: int = verification.calc_json_data_entry_count()
        DATABASE_ATTACHED: bool = verification.verify_database_attached()
        if DATABASE_ATTACHED: 
            DATABASE_ENTRY_COUNT: int = verification.calc_database_entry_count()


# Calling session instance:
SESSION = Session()

