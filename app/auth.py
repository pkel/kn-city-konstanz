import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

blueprint = Blueprint('auth', __name__, url_prefix=None)

@blueprint.post('/registrieren')
def register_post():
    username = request.form['username']
    password = request.form['password']

    # TODO: input is lost on failed attempt; retain!

    invalid_input = False

    if not username:
        invalid_input = True
        flash('Ohne Nutzername geht es nicht!')

    if not password:
        invalid_input = True
        flash('Ohne Passwort geht es nicht!')

    if invalid_input:
        return redirect(url_for("auth.register"))

    db = get_db()
    try:
        db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
                )
        db.commit()
    except db.IntegrityError:
        flash(f"Der Nutzername „{username}” ist bereits vergeben!")
        return redirect(url_for("auth.register"))
    else:
        flash(f"Registrierung erfolgreich. Sie können sich jetzt anmelden!")
        return redirect(url_for("auth.login"))

@blueprint.get('/registrieren')
def register():
    return render_template('register.html')


@blueprint.post('/einloggen')
def login_post():
    username = request.form['username']
    password = request.form['password']

    # TODO: input is lost on failed attempt; retain!

    invalid_input = False

    if not username:
        invalid_input = True
        flash('Ohne Nutzername geht es nicht!')

    if not password:
        invalid_input = True
        flash('Ohne Passwort geht es nicht!')

    if invalid_input:
        session.clear()
        return redirect(url_for("auth.login"))

    db = get_db()
    user = db.execute(
        'SELECT id, password FROM users WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        # prevent timing attack
        # (we do not want to reveal whether a user exists or not)
        check_password_hash('dummy', 'dummy')
        valid_user = False
    else:
        valid_user = check_password_hash(user['password'], password)

    if not valid_user:
        flash("Ungültige Zugangsdaten!")
        return redirect(url_for("auth.login"))

    session.clear() # nested login
    session['user_id'] = user['id']
    return redirect(url_for('index'))

@blueprint.get('/einloggen')
def login():
    return render_template('login.html')

# This runs before all requests and ensures that g.user is set correctly.
@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@blueprint.route('/abmelden')
def logout():
    was_logged_in = g.user is None

    session.clear()

    if was_logged_in:
        flash('Sie sind nicht eingeloggt; Abmelden nicht möglich!')
    else:
        flash('Sie haben sich erfolgreich abgemeldet.')

    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # TODO login should redirect to the requested & restricted page
        if g.user is None:
            flash("Diese Seite ist nur für eingeloggte Nutzer zugänglich.")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
