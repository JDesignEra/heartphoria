import re
import os
from datetime import datetime

import requests
from flask import Blueprint, g, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from heartphoria import app
from heartphoria import db
from heartphoria.models import User, Appointment, Reminder, History
from heartphoria.mail import Mail
from heartphoria.blueprints.auth import login_required

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/<int:user_id>')
@login_required
def index(user_id):
    image = None

    if g.user['id'] != user_id and g.user['role'] != 'admin':
        return redirect(url_for('general.index'))

    try:
        if requests.get(request.url_root + 'static/images/dp/%s.png' % g.user['id']).status_code == 200:
            image = url_for('static', filename='images/dp/%s.png' % g.user['id']) + '?v=%s' % datetime.now().time()
    except requests.exceptions.ConnectionError:
        pass

    bmi = {
        'index': None if g.user['weight'] == 0 or g.user['height'] == 0 else round(g.user['weight'] / (g.user['height'] / 100 * g.user['height'] / 100))
    }

    if bmi['index']:
        if bmi['index'] >= 27.5:
            bmi['text'] = 'HIGH RISK'
        elif bmi['index'] >= 23:
            bmi['text'] = 'MODERATE RISK'
        elif bmi['index'] >= 18.5:
            bmi['text'] = 'LOW RISK'
        else:
            bmi['text'] = 'Risk Of Nutritional Deficiency'

    reminders = Reminder.query.filter_by(user_id=user_id).order_by(Reminder.time).limit(10).all()
    appointments = Appointment.query.filter_by(user_id=user_id).order_by(Appointment.date_time.desc()).limit(10).all()
    histories = History.query.filter_by(user_id=user_id).order_by(History.date.desc()).limit(10).all()

    return render_template('user/index.html', title=g.user['name'], reminders=reminders, appointments=appointments, histories=histories, bmi=bmi, image=image)


@blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    image = None
    name = None
    gender = None
    dob = None
    height = None
    weight = None
    email = None
    errors = {}

    try:
        if requests.get(request.url_root + 'static/images/dp/%s.png' % g.user['id']).status_code == 200:
            image = url_for('static', filename='images/dp/%s.png' % g.user['id']) + '?v=%s' % datetime.now().time()
    except requests.exceptions.ConnectionError:
        pass

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']

            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + str(g.user['id']) + '.png'))

            return redirect(url_for('.index', user_id=g.user['id']))
        elif request.form.get('remove'):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'] + str(g.user['id']) + '.png'))

            return redirect(url_for('.index', user_id=g.user['id']))
        else:
            name = request.form.get('name')
            gender = request.form.get('gender')
            dob = request.form.get('dob')
            height = request.form.get('height')
            weight = request.form.get('weight')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm = request.form.get('confirm')
            data = {}

            if name:
                if not re.match(r'[a-zA-Z]+(?:\s[a-zA-Z]+)*$', name):
                    errors['name'] = 'Name is invalid'
                else:
                    data['name'] = name

            if gender:
                data['gender'] = gender
            else:
                errors['gender'] = 'Gender is required'

            if dob:
                try:
                    data['dob'] = datetime.strptime(dob, '%Y-%m-%d').date()
                except ValueError:
                    errors['dob'] = 'Invalid date format'

            if height:
                data['height'] = height

            if weight:
                data['weight'] = weight

            if email:
                if not re.match(r"[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
                    errors['email'] = 'Email address is invalid.'
                elif g.user['email'] != email and not User.query.filter_by(email=email).first() is not None:
                    errors['email'] = email + ' already exists'
                else:
                    data['email'] = email.lower()

            if password:
                if not re.match(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$', password):
                    errors['password'] = 'Password is invalid'
                elif not confirm:
                    errors['confirm'] = 'Please re-enter password for confirmation'
                elif not password == confirm:
                    errors['confirm'] = 'Passwords do not match'
                else:
                    data['password'] = generate_password_hash(password)

            if not errors:
                if (not name or name == g.user['name']) and \
                        (not gender or gender == g.user['gender']) and \
                        (not dob or dob == str(g.user['dob'])) and \
                        (not height or height == str(g.user['height'])) and \
                        (not weight or weight == str(g.user['weight'])) and \
                        (email == g.user['email']):
                    errors['all'] = 'Nothing to update'
                else:
                    if User.query.filter_by(id=g.user['id']).first() is not None:
                        User.query.filter_by(id=g.user['id']).update(data)
                        db.session.commit()

                    Mail().send_mail(
                        [g.user['email'], email] if email else g.user['email'],
                        '[Heartphoria] Account Details Changed',
                        render_template('email/edit.html', name=name, gender=gender, dob=dob, height=height, weight=weight, email=email, password=password)
                    )

                    user = User.query.filter_by(id=g.user['id']).first()

                    if user:
                        user = user.__dict__

                        if '_sa_instance_state' in user:
                            del user['_sa_instance_state']

                        g.user = user

                    return redirect(url_for('.index', user_id=g.user['id']))

    return render_template('user/edit.html', title='Edit Profile', name=name, gender=gender, dob=dob, height=height, weight=weight, email=email, errors=errors, image=image)
