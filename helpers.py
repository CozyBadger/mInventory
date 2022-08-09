import re
import sqlite3

def db_connect(db):
    try:
        connection = sqlite3.connect(db)
    # TODO: More meaningful exception handling
    except:
        raise

    return connection


def format_items(items):
    """ Takes the list of query results from the DB

        returns a list of dictionaries of all items
    """
    item_list = []
    for item in items:
        item_entry = {}

        item_entry["id"] = item[0]
        item_entry["item_name"] = item[1]
        item_entry["amount"] = item[2]
        item_entry["unit"] = item[3]

        item_list.append(item_entry)

    return item_list


def validate_string(string):
    """ Check if a string only contains allowed characters

        returns True if string is valid
        returns False if string has special characters or numbers
    """
    allowed_pattern = "^[aA-zZ]+"

    if not re.match(allowed_pattern, string):
        return False

    return True
