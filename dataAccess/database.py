import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


# Connect to database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# Close database connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Re-initialize database (Clear existing data and creat new tables).
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
# Re-initialize database (Clear existing data and create new tables).
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


# Register database functions with the Flask app.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
