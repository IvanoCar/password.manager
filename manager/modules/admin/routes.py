from flask import Blueprint, render_template, request
from pyperclip import copy
from threading import Thread
from manager.modules.utils.utility import Utils
from manager import DATABASE, ESSENTIALS

admin = Blueprint('admin', __name__, url_prefix='/dashboard')


@admin.before_request
def check():
    try:
        if not ESSENTIALS['session']['logged-in']:
            return render_template('login.html', notlgin=True)
    except KeyError:
        return render_template('login.html', notlgin=True)


# add message box and message
@admin.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', services=DATABASE.storage['services'])


@admin.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        new = {
            "group": "",
            "username": request.form['username'],
            "name": request.form['servis'],
            "id": str(len(DATABASE.storage['services'])),
            "password": request.form['password']
        }
        DATABASE.storage['services'].append(new)
        DATABASE.save_database()
        message = 'Novi unos spremljen.'
        return render_template('dashboard.html', services=DATABASE.storage['services'], msgNeeded=True, msg=message)


@admin.route('/copy/<pid>', methods=['GET'])
def copy_pwd(pid):
    try:
        copy(DATABASE.storage['services'][int(pid)]['password'])
        Thread(target=Utils.clear_clipboard).start()
        message = 'Lozinka za servis %s je kopirana sljedećih 15 sekundi.' % DATABASE.storage['services'][int(pid)][
            'name']
        return render_template('dashboard.html', services=DATABASE.storage['services'], msgNeeded=True, msg=message)
    except (IndexError, KeyError):
        print('error')
        return render_template('dashboard.html', services=DATABASE.storage['services'])


@admin.route('/edit', methods=['POST'])
def save_edit():
    pid = request.form['id']
    enew = {
        "group": "",
        "username": request.form['username'],
        "name": request.form['servis'],
        "id": pid,
        "password": request.form['password']
    }
    DATABASE.storage['services'][int(pid)] = enew
    DATABASE.save_database()
    message = 'Unos je promijenjen.'
    return render_template('dashboard.html', services=DATABASE.storage['services'], msgNeeded=True, msg=message)


@admin.route('/edit/<pid>', methods=['GET'])
def edit(pid):
    if request.method == 'GET':
        return render_template('edit.html', service=DATABASE.storage['services'][int(pid)])


@admin.route('/delete/<pid>', methods=['GET'])
def delete(pid):
    try:
        if len(DATABASE.storage['services']) is 1:
            del DATABASE.storage['services'][0]
        else:
            del DATABASE.storage['services'][int(pid)]
        DATABASE.save_database()
        message = 'Uspješno obrisano.'
        return render_template('dashboard.html', services=DATABASE.storage['services'], msgNeeded=True, msg=message)
    except (IndexError, KeyError):
        return render_template('dashboard.html', services=DATABASE.storage['services'])
