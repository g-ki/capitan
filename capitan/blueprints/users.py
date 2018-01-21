from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

url_prefix = '/users'
bp = Blueprint('users', __name__)


@bp.route('/')
def users():
    return "[Users]"


@bp.route('/new')
def new_node():
    return "New User"


@bp.route('/<path:user_id>')
def user(user_id):
    return f"User with {user_id}"
