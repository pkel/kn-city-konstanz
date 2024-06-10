from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db
from app.auth import login_required

blueprint = Blueprint('booking', __name__, url_prefix=None)

@blueprint.get('/reservieren')
@login_required
def reserve():
    return render_template('reserve.html')
