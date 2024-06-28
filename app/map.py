from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db
from app.auth import login_required

blueprint = Blueprint('map', __name__, url_prefix=None)

@blueprint.get('/map')
def reserve():
    return render_template('map.html')
