from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import json
from app.db import get_db
from app.auth import login_required
from datetime import datetime

blueprint = Blueprint('booking', __name__, url_prefix=None)

@blueprint.get('/reservieren')
@login_required
def reserve():
    return render_template('reserve.html')

# Filter for parking slot
def filterBooking(forName=None):
    selectStatement = "SELECT id, companyId, startDateTime, endDateTime FROM booking"
    if forName is None:
        return (selectStatement,
                ())
    else:
        return (selectStatement + " WHERE parkingSpot = ?",
                (forName,))

# Query for a list of bookings for parking slots with filter applied
def searchBooking(filter):
    db = get_db()
    try:
        return db.execute(filter[0], filter[1]).fetchall()
    except db.IntegrityError:
        flash(f"Unbekannter Parkplatz „{parkingspot}” erkannt!")
        return []


@blueprint.get('/getBookings')
# @login_required
def getBookings():
        # companyId = session['username']
    if "companyId" in request.args.keys():
        companyId = request.args.get("companyId")
    if "parkingSpot" in request.args.keys():
        parkingSpot = request.args.get("parkingSpot")
    else:
        parkingSpot = None

    bookings = searchBooking(filterBooking(forName=parkingSpot))
    if bookings is None:
        flash(f"Keine Buchungen gefunden!")
        return []
    
    bookingList = [{
        "isMine": True if companyId == each["companyId"] else False,
        "startDateTime": each["startDateTime"],
        "endDateTime": each["endDateTime"]
    } for each in bookings]

    return jsonify(bookingList)

def alreadyBooked(parkingSpot, startDateTime, endDateTime):
    bookings = searchBooking(filterBooking(forName=parkingSpot))
    if bookings is None or len(bookings) == 0:
        return False
    for each in bookings:
        oldStart = datetime.fromisoformat(each["startDateTime"])
        oldEnd = datetime.fromisoformat(each["endDateTime"])
        newStart = datetime.fromisoformat(startDateTime)
        newEnd = datetime.fromisoformat(endDateTime)
        # End between old start and end
        if  newEnd <= oldEnd and newEnd >= oldEnd:
            return True
        # Start between old start and end
        if newStart >= oldStart and newStart <= oldEnd:
            return True
        # New Range contains old Range
        if newStart <= oldStart and newEnd >= oldStart:
            return True
        # New Range starts in old Range
        if newStart >= oldStart and newStart <= oldEnd:
            return True
    return False

@blueprint.post('/createBooking')
# @login_required
def book():
    companyId = request.form['companyId']
    startDateTime = request.form['startDateTime']
    endDateTime = request.form['endDateTime']
    parkingSpot = request.form["parkingSpot"]

    print(companyId,startDateTime,endDateTime,parkingSpot)

    if alreadyBooked(parkingSpot, startDateTime, endDateTime):
        flash(f"Der Parkplat „{parkingSpot}” ist bereits vergeben!")
        return {}
    db = get_db()
    try:
        db.execute(
                "INSERT INTO booking (companyId, startDateTime, endDateTime, parkingspot) VALUES (?,?,?,?)",
                (companyId, startDateTime, endDateTime, parkingSpot),
                )
        db.commit()
        return {}
    except db.IntegrityError:
        flash(f"Buchung konnte nicht durchgeführt werden!")
        return {}
    else:
        flash(f"Buchung erfolgreich.")
        return {}
    
    return {}