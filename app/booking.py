from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db
from app.auth import login_required

blueprint = Blueprint('booking', __name__, url_prefix=None)

@blueprint.get('/reservieren/zone/<zone>')
@login_required
def form(zone):
    return render_template('reserve.html')
