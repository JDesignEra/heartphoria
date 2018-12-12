from flask import Blueprint, render_template

blueprint = Blueprint('general', __name__)

@blueprint.route('/')
def index():
    year=None
    return render_template('index.html', title='Home Page', year=year)
