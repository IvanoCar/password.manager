import os
import sys
from flask import Flask
import webview
from threading import Thread
import time
from manager.modules.utils.encription import Encryption
from manager.modules.utils.phelper import resource_path

if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

encryption = Encryption(None, None)

is_run = False
4
app.secret_key = 'Wg3koVqW=O=I)UU151561651516%$E#$W"$#$%(' # implement rotation
loc = os.environ['HOMEPATH'] + '/Documents'
bp_path = loc + '/database.pmanager'
from manager.modules.utils.database import Database

DATABASE = Database()
DATABASE.location = bp_path

if os.path.exists(bp_path):
    first_open = False
else:
    first_open = True

ESSENTIALS = {
    'database': bp_path,
    'session': {},
    'password-master': '',
    'first-open': first_open
}

from manager.modules.admin.routes import admin
from manager.modules.main.routes import main
from manager.modules.generator.routes import generator

app.register_blueprint(admin)
app.register_blueprint(main)
app.register_blueprint(generator)

# port = random.randint(1025, 9999)
port = 5000


# TODO:
# reorganize this file


def run():
    app.run(port=port)


if __name__ == '__main__':
    t = Thread(target=run).start()
    time.sleep(0.2)
    webview.create_window('Password Manager', 'http://127.0.0.1:%s/' % port, width=850, height=420, resizable=False)
