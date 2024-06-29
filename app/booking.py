from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db
from app.auth import login_required

from . import map

blueprint = Blueprint('booking', __name__, url_prefix=None)

@blueprint.get('/reservieren/zone/<int:zone_id>')
@login_required
def form(zone_id):
    zone = map.zone(zone_id)
    return render_template('reserve.html', zone=zone)
