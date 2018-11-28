from flask import Blueprint, render_template
from pyperclip import copy
from manager.modules.utils.utility import Utils
from threading import Thread
from manager import ESSENTIALS

generator = Blueprint('generator', __name__, url_prefix='/generator')


@generator.before_request
def check():
    try:
        if not ESSENTIALS['session']['logged-in']:
            return render_template('login.html', notlgin=True)
    except KeyError:
        return render_template('login.html', notlgin=True)


@generator.route('/', methods=['GET'])
def generate():
    return render_template('generate.html', generated=False)


@generator.route('/new', methods=['POST'])
def new_password():
    result = Utils.generate_pass()
    copy(result)
    Thread(target=Utils.clear_clipboard).start()
    return render_template('generate.html', generated=True, password=result)
