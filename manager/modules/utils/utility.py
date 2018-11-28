import json
from pyperclip import copy
import time
import secrets
import string


class Utils:

    @staticmethod
    def clear_clipboard():
        time.sleep(15)
        copy("")

    @staticmethod
    def generate_pass():
        return ''.join(
            secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + '$%!#@') for _ in range(8))
