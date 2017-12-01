import os, sys

def default_settings_db_path():
    return os.path.join(os.path.dirname(__file__), "DEFAULT_DB_SETTINGS.cfg")