import functools
import re

from flask import Blueprint, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from heartphoria.mail import send_mail
from heartphoria.db import get_db

blueprint = Blueprint('auth', __name__)


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    name = None
    email = None
    errors = {}

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        db = get_db()

        if not name:
            errors['name'] = 'Name is required.'
        elif not re.match(r'[a-zA-Z]+(?:\s[a-zA-Z]+)*$', name):
            errors['name'] = 'Name is invalid.'

        if not email:
            errors['email'] = 'Email address is required.'
        elif not re.match(r"[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
            errors['email'] = 'Email address is invalid.'
        elif db.execute('SELECT id FROM user WHERE email = ?', [email]).fetchone() is not None:
            errors['email'] = email + ' already exists.'

        if not password:
            errors['password'] = 'Password is required.'
        elif not re.match(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$', password):
            errors['password'] = 'Password is invalid.'
        elif not confirm:
            errors['confirm'] = 'Please re-enter password for confirmation.'
        elif not password == confirm:
            errors['confirm'] = 'Passwords do not match.'

        if not errors:
            db.execute('INSERT INTO user (email, password, name, role) VALUES (?, ?, ?, ?)', [email.lower(), generate_password_hash(password), name, 'user'])
            db.commit()

            send_mail(
                email,
                '[Heartphoria] Sign Up Successful',
                render_template('email/signup.html', name=name, email=email, password=password).replace('\n', ''),
            )

            return redirect(url_for('.login'))

    return render_template('auth/signup.html', title='Sign up', name=name, email=email, errors=errors)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    email = None
    errors = {}

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = get_db()

        if not email:
            errors['email'] = 'Email address is required.'
        else:
            user = db.execute('SELECT * FROM user WHERE email = ?', [email.lower()]).fetchone()

            if user is None:
                errors['email'] = email + ' does not exist.'
            elif not check_password_hash(user['password'], password):
                errors['password'] = 'Password is incorrect.'

        if not errors:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('general.index'))

    return render_template('auth/login.html', title='Log in', email=email, errors=errors)


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', [user_id]).fetchone()


@blueprint.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('general.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
