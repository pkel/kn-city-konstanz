import click
import sqlite3
from flask import current_app, g


def get_db():
    if 'db' not in g:
        database = current_app.config['DATABASE']
        current_app.logger.debug(f"connect database {database}")
        g.db = sqlite3.connect(
            database,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('init-db')
def init_db():
    """Clear the existing data and create new tables."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    current_app.logger.info('database initialized')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
