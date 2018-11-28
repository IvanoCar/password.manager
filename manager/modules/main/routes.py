import json
import os

from flask import Blueprint, render_template, request
from manager import ESSENTIALS, encryption, DATABASE

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    if ESSENTIALS['first-open']:
        return render_template('login.html', submitText="Registriraj se", link='/register')
    else:
        return render_template('login.html', submitText='Prijava', link='/login')


@main.route('/logout', methods=['GET'])
def logout():
    ESSENTIALS['session'] = {}
    return render_template('login.html', submitText='Prijava', link='/login', logout=True)


@main.route('/login', methods=['POST'])
def login():
    f_user = request.form['usr']
    f_pwd = request.form['pwd']

    encryption.username = f_user
    encryption.password = f_pwd

    with open(DATABASE.location, 'r', encoding='utf-8') as f:
        db = f.read()

    try:
        data = encryption.decrypt(db.encode('utf-8'))
        DATABASE.storage = json.loads(data)
    except json.JSONDecodeError:
        return render_template('login.html', error=True, submitText='Prijava', link='/login')
    except UnicodeDecodeError:
        pass
    except Exception as e:  # decryprt error - except exact errors: TODO
        print('Decription error', e)
        os.remove(DATABASE.location)
        return render_template('login.html', submitText="Registriraj se", link='/register',
                               errorBP=True)

    if f_pwd == DATABASE.storage['login-data']['password'] and f_user == DATABASE.storage['login-data']['username']:
        ESSENTIALS['session']['user'] = f_user
        ESSENTIALS['session']['logged-in'] = True
        ESSENTIALS['password-master'] = f_pwd
        return render_template('dashboard.html', services=DATABASE.storage['services'])
    else:
        return render_template('login.html', error=True, submitText='Prijava', link='/login')


@main.route('/register', methods=['POST'])
def register():
    f_user = request.form['usr']
    f_pwd = request.form['pwd']
    DATABASE.storage['login-data'] = {
        'password': f_pwd,
        'username': f_user,
    }

    DATABASE.storage['services'] = []

    encryption.username = f_user
    encryption.password = f_pwd

    ESSENTIALS['session']['user'] = f_user
    ESSENTIALS['session']['logged-in'] = True
    ESSENTIALS['password-master'] = f_pwd

    DATABASE.save_database()

    return render_template('dashboard.html', services=DATABASE.storage['services'])
