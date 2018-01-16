from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

bp = Blueprint('capitan', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #
        # TODO:
        # validate and login ..
        #
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('capitan.dashboard'))
    return render_template('login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('capitan.login'))


@bp.route('/')
def dashboard():
    return "Dashboard ..."


@bp.route('/404')
def page_not_found():
    current_app.logger.error('this is error')
    return render_template('page_not_found.html'), 404
