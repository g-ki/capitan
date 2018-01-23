from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from sqlite3 import dbapi2 as sqlite3
from capitan.blueprints.login_required import login_required
import hashlib

bp = Blueprint('database', __name__)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    create_user('admin', 'admin')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def create_user(username, password):
    db = get_db()
    hash_pass = hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

    db.execute('insert into users (username, password) values (?, ?)', [username, hash_pass])
    db.commit()
