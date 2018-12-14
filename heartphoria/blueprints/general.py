from flask import Blueprint, g, render_template

from heartphoria.db import get_db

blueprint = Blueprint('general', __name__)

@blueprint.route('/')
def index():
    reminders = None
    appointments = None

    if g.user:
        db = get_db()

        reminders = db.execute('SELECT * FROM reminder WHERE user_id = ? ORDER BY time LIMIT 5', [g.user['id']]).fetchall()
        appointments = db.execute('SELECT * FROM appointment WHERE user_id = ? AND date_time > datetime("now") ORDER BY date_time DESC LIMIT 5', [g.user['id']]).fetchall()

    return render_template('index.html', title='Home Page', reminders=reminders, appointments=appointments)
