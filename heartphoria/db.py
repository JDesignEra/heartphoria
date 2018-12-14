import click
from datetime import datetime
import sqlite3

from flask import g
from flask.cli import with_appcontext

from heartphoria import app

def init_app():
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def get_db():
    if 'db' not in g:
        sqlite3.register_converter('time', convert_time)
        g.db = sqlite3.connect('heartphoria.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def convert_time(s):
    return datetime.strptime(s.decode('utf-8'), '%H:%M:%S').time()

