import functools
import re
import random
import string

import requests
from flask import Blueprint, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from heartphoria import db
from heartphoria.models import User
from heartphoria.mail import send_mail

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

        if not name:
            errors['name'] = 'Name is required.'
        elif not re.match(r'[a-zA-Z]+(?:\s[a-zA-Z]+)*$', name):
            errors['name'] = 'Name is invalid'

        if not email:
            errors['email'] = 'Email is required.'
        elif not re.match(r"[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
            errors['email'] = 'Email is invalid.'
        elif User.query.filter_by(email=email.lower()).first() is not None:
            errors['email'] = email + ' already exists'

        if not password:
            errors['password'] = 'Password is required.'
        elif not re.match(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$', password):
            errors['password'] = 'Password is invalid'
        elif not confirm:
            errors['confirm'] = 'Please re-enter password for confirmation'
        elif not password == confirm:
            errors['confirm'] = 'Passwords do not match'

        if not errors:
            user = User(email=email.lower(), password=generate_password_hash(password), name=name, role='user')
            db.session.add(user)
            db.session.commit()

            send_mail(
                email,
                '[Heartphoria] Sign Up Successful',
                render_template('email/signup.html', name=name, email=email.lower(), password=password)
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

        if not email:
            errors['email'] = 'Email is required'
        else:
            user = User.query.filter_by(email=email.lower()).first()

            if user is None:
                errors['email'] = email + ' does not exist'
            elif not check_password_hash(user.password, password):
                errors['password'] = 'Password is incorrect'

        if not errors:
            session.clear()
            session['user_id'] = user.id

            return redirect(url_for('general.index'))

    return render_template('auth/login.html', title='Login', email=email, errors=errors)


@blueprint.route('/forgot', methods=['GET', 'POST'])
def forgot():
    email = None
    errors = {}

    if request.method == 'POST':
        link = None
        email = request.form.get('email')

        if not email:
            errors['email'] = 'Email is required'
        else:
            user = User.query.filter_by(email=email.lower()).first()

            if user is None:
                errors['email'] = email + ' is not registered'
            else:
                fcode = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(8))

                user.fcode = fcode
                db.session.commit()

                try:
                    if requests.get('https://heartphoria.ap.ngrok.io/').status_code == 200:
                        link = 'https://heartphoria.ap.ngrok.io/change/' + str(user.id) + '/' + fcode
                except requests.ConnectionError:
                    if link is None:
                        link = request.url_root + 'change/' + str(user.id) + '/' + fcode

                send_mail(
                    email,
                    '[Heartphoria] Forgot Password',
                    render_template('email/forgot.html', link=link)
                )

                return render_template('auth/forgot_success.html')

    return render_template('auth/forgot.html', title='Forgot Password', email=email, errors=errors)


@blueprint.route('/forgot/<int:user_id>')
def resend_forgot(user_id):
    link = None

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return redirect(url_for('auth.forgot'))
    else:
        fcode = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(8))

        user.fcode = fcode
        db.session.commit()

        try:
            if requests.get('https://heartphoria.ap.ngrok.io/').status_code == 200:
                link = 'https://heartphoria.ap.ngrok.io/change/' + str(user.id) + '/' + fcode
        except requests.ConnectionError:
            if link is None:
                link = request.url_root + 'change/' + str(user.id) + '/' + fcode

        send_mail(
            user.email,
            '[Heartphoria] Forgot Password',
            render_template('email/forgot.html', link=link)
        )

    return render_template('auth/forgot_success.html')


@blueprint.route('/change/<int:user_id>/<string:fcode>', methods=['GET', 'POST'])
def change(user_id, fcode):
    errors = {}

    user = User.query.filter_by(id=user_id, fcode=fcode).first()

    if user is None:
        return render_template('auth/change_error.html', user_id=user_id)

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not password:
            errors['password'] = 'Password is required'
        elif not re.match(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$', password):
            errors['password'] = 'Password is invalid'
        elif not confirm:
            errors['confirm'] = 'Please re-enter password for confirmation'
        elif not password == confirm:
            errors['confirm'] = 'Passwords do not match'

        if not errors:
            user.password = generate_password_hash(password)
            user.fcode = None
            db.session.commit()

            send_mail(
                user.email,
                '[Heartphoria] Password Changed',
                render_template('email/change.html', password=password)
            )

            return render_template('auth/change_success.html', title='Change Password Successful')

    return render_template('auth/change.html', title='Change Password', errors=errors)


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user = User.query.filter_by(id=user_id).first()

        if user:
            user = user.__dict__

            if '_sa_instance_state' in user:
                del user['_sa_instance_state']

            g.user = user


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
