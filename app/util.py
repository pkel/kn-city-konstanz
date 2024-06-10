import app
import sqlite3

def sqlite3_connect(filename):
    """
    Wrapper around sqlite3.connect that enables convenience features.
    """
    app.logger.debug(f"connect to database '{filename}'")
    db = sqlite3.connect(filename, 10)
    db.execute("PRAGMA foreign_keys = ON")
    return db

def with_database():
    def decorator(f):
        @click.option(
            "--database",
            type=click.Path(exists=True),
            envvar="KNCL_DATABASE",
            default="app.db",
            help="SQLite database to use. Also sourced from $KNCL_DATABASE.",
        )
        @wraps(f)
        def wrapper(database, **kwds):
            app.db = sqlite3_connect(database)
            with app.db:
                app.settings = {}
                for k, v in app.db.execute("SELECT key, value FROM settings").fetchall():
                    try:
                        val = json.loads(v)
                    except ValueError:
                        warnings.warn(
                            f"Setting {k} is not a valid JSON value: {v!r}. It will be ignored."
                        )
                        continue
                    app.settings[k] = val
            return f(**kwds)

        return wrapper

    return decorator
