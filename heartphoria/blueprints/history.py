from datetime import datetime

from flask import Blueprint, g, render_template, request

from heartphoria import db
from heartphoria.models import History
from heartphoria.blueprints.auth import login_required

blueprint = Blueprint('history', __name__, url_prefix='/history')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    date = None
    description = None
    errors = {}

    if request.method == 'POST':
        date = request.form.get('date')
        description = request.form.get('description')

        if not date:
            errors['date'] = 'Date is required.'

        if not description:
            errors['description'] = 'Description is required.'

        if not errors:
            history = History(user_id=g.user['id'], date=datetime.strptime(date, '%Y-%m-%d').date(), description=description)
            db.session.add(history)
            db.session.commit()

    histories = History.query.filter_by(user_id=g.user['id']).order_by(History.date.desc()).all()

    return render_template('history/index.html', title='Medical History', date=date, description=description, errors=errors, histories=histories)
