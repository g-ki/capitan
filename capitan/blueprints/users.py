from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from capitan.blueprints.database import get_db, create_user
from capitan.blueprints.login_required import login_required

url_prefix = '/users'
bp = Blueprint('users', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    cur = db.execute('select username from users order by id desc')
    users = list(map(lambda user: tuple(user)[0], cur.fetchall()))

    return render_template('users/index.html', users=users)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    error = session.pop('error_message', None)
    return render_template('users/new.html', error=error)


@bp.route('/new', methods=['POST'])
@login_required
def create():
    username = request.form['username']
    password = request.form['password']

    if len(username) < 3 or len(password) < 3:
        session['error_message'] = "Username and password must be atleast 4 symbols"
        return redirect(url_for('.new'))

    create_user(username, password)

    return redirect(url_for('.index'))


# @bp.route('/<path:user_id>')
# def user(user_id):
#     return f"User with {user_id}"
