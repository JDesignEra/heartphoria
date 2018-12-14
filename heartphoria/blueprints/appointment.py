from datetime import datetime

from flask import Blueprint, g, redirect, render_template, request, url_for

from heartphoria.blueprints.auth import login_required
from heartphoria.db import get_db

blueprint = Blueprint('appointment', __name__, url_prefix='/appointment')

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():

    return render_template('appointment/index.html')
