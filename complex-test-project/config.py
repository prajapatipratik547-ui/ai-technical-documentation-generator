APP_NAME = "AI Calculator"
VERSION = "1.0.0"
DEFAULT_OPERATION = "add"


def get_app_info():
    """Return basic application information."""

    return {
        "name": APP_NAME,
        "version": VERSION,
        "default_operation": DEFAULT_OPERATION,
    }