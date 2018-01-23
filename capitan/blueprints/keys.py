from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from capitan.blueprints.login_required import login_required
from capitan.blueprints.database import get_db

url_prefix = '/keys'
bp = Blueprint('keys', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('keys/index.html', keys=user_keys())


@bp.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('keys/new.html')


@bp.route('/new', methods=['POST'])
@login_required
def create():
    db = get_db()
    db.execute('insert into keys (key, user_id) values (?, ?)', [request.form['key'], session.get('user_id')])
    db.commit()

    return redirect(url_for('.index'))


def user_keys():
    db = get_db()
    cur = db.execute("select key from keys where user_id=?", [session.get('user_id')])
    keys = list(map(lambda key: tuple(key)[0], cur.fetchall()))

    return keys
