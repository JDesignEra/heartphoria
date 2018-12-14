from datetime import datetime

from flask import Blueprint, g, redirect, render_template, request, url_for

from heartphoria.blueprints.auth import login_required
from heartphoria.db import get_db

blueprint = Blueprint('reminder', __name__, url_prefix='/reminder')

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():


    return render_template('reminder/index.html')
