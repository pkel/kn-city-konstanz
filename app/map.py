from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db
from app.auth import login_required

zones = []

def add_zone(*args, name, longitude, latitude):
    z = dict(id=len(zones), name=name, longitude = longitude, latitude = latitude)
    zones.append(z)

add_zone(name="Max-Stromeyer-Straße 176", longitude=9.150573142319644, latitude=47.67961017045168)
add_zone(name="Dettinger Straße", longitude=9.142530658669918, latitude=47.694316576346765)
add_zone(name="Schwaketenstraße", longitude=9.159333187466896, latitude=47.68802596035806)
add_zone(name="Konrad-Zuse-Straße", longitude=9.161475478573882, latitude=47.67690602262776)
add_zone(name="An der Linde", longitude=9.188143552111852, latitude=47.674525329673415)
add_zone(name="Luisenstraße", longitude=9.185555294956334, latitude=47.67080617335832)
add_zone(name="Lorettosteig", longitude=9.198787053233458, latitude=47.67538410940641)
add_zone(name="Mainaustraße 147", longitude=9.202239181520447, latitude=47.68169558289792)
add_zone(name="Mainaustraße 234", longitude=9.193330388228206, latitude=47.69285229918978)
add_zone(name="Gartenstraße", longitude=9.1630646686759, latitude=47.66646372589333)
add_zone(name="Rheingutstaße", longitude=9.166924063131988, latitude=47.667281151838125)

def zone(id:int):
    assert id == zones[id]['id']
    return zones[id]

blueprint = Blueprint('map', __name__, url_prefix=None)

@blueprint.get("/")
def map():
    return render_template('map.html', zones=zones)
