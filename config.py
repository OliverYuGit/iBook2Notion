import abc
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    

class Config(metaclass=Singleton):

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.book_sqlite_path = os.getenv("BOOK_SQLITE_PATH")
        self.annotation_sqlite_path = os.getenv("ANNOTATION_SQLITE_PATH")
        self.zapier_api_key = os.getenv("ZAPIER_API_KEY")
        self.max_notes4ai = int(os.getenv("MAX_NOTES4AI", 5))
        self.mark_file = os.getenv("MARK_FILE")

        self.notion_token = os.getenv("NOTION_TOKEN")
        self.notion_version = os.getenv("NOTION_VERSION")
        self.note_db_id = os.getenv("NOTE_DB_ID")
        self.note_title_field = os.getenv("NOTE_TITLE_FIELD")
        self.note_location_field = os.getenv("NOTE_LOCATION_FIELD")
        self.note_custom_fields = json.loads(os.getenv("NOTE_CUSTOM_FIELDS") or '{}')