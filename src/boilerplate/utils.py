from datetime import datetime, timezone


def get_uk_time():
    """
    Define the UK timezone offset (+0100 for BST, +0000 for GMT)
    """
    return datetime.now(timezone.utc)
