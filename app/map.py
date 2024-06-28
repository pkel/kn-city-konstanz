from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db
from app.auth import login_required

blueprint = Blueprint('map', __name__, url_prefix=None)

@blueprint.get('/map')
def map():
    return render_template('map.html')

@blueprint.get("/zone/<int:zone_id>")
def booking(zone_id):

    return render_template('booking.html', zone=zone_id)
