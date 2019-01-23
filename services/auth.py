import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bson.objectid import ObjectId
from services.db import add_user, find_user_by_name, find_user_by_id

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not add_user(username, generate_password_hash(password)):
            error = 'Username repeated.'

        if error is None:
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = find_user_by_name(username)
        print('get here!')
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = str(user['_id'])
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# use session to store the user infos
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = find_user_by_id(ObjectId(user_id))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# utils for other applications (decorator)
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
