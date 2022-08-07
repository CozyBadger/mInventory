import re

def validate_string(string):
    """ Check if a string only contains allowed characters

        returns True if string is valid
        returns False if string has special characters or numbers
    """
    allowed_pattern = "^[aA-zZ]+"

    if not re.match(allowed_pattern, string):
        return False

    return True
