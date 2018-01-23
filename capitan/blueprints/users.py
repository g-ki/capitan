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
    return render_template('users/new.html')


@bp.route('/new', methods=['POST'])
@login_required
def create():
    create_user(request.form['username'], request.form['password'])

    return redirect(url_for('.index'))


# @bp.route('/<path:user_id>')
# def user(user_id):
#     return f"User with {user_id}"
