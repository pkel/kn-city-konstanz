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
    selectStatement = "SELECT id, username, startRange, endRange FROM booking"
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
    if "parkingSpot" in request.args.keys():
        parkingSpot = request.args.get("parkingSpot")
    else:
        parkingSpot = None

    bookings = searchBooking(filterBooking(forName=parkingSpot))
    if bookings is None:
        flash(f"Keine Buchungen gefunden!")
        return []
    
    bookingList = [{
        "username": each["username"],
        "startRange": each["startRange"],
        "endRange": each["endRange"]
    } for each in bookings]

    return jsonify(bookingList)

def alreadyBooked(parkingSpot,startRange,endRange):
    bookings = searchBooking(filterBooking(forName=parkingSpot))
    if bookings is None or len(bookings) == 0:
        return False
    for each in bookings:
        oldStart = datetime.fromisoformat(each["startRange"])
        oldEnd = datetime.fromisoformat(each["endRange"])
        newStart = datetime.fromisoformat(startRange)
        newEnd = datetime.fromisoformat(endRange)
        # End between old start and end
        if  newEnd <= oldEnd and newEnd >= oldEnd:
            return True
        # Start between old start and end
        if newStart >= oldStart and newStart <= oldEnd:
            return True
        if newStart <= oldStart and newEnd >= oldStart:
            return True
        if newStart >= oldStart and newStart <= oldEnd:
            return True
    return False

@blueprint.post('/book')
# @login_required
def book():
    username = session['username']
    if "parkingSpot" in request.args.keys():
        parkingSpot = request.args.get("parkingSpot")
    if "startRange" in request.args.keys():
        startRange = request.args.get("startRange")
    if "endRange" in request.args.keys():
        endRange = request.args.get("endRange")

    if alreadyBooked(parkingSpot,startRange,endRange):
        flash(f"Der Parkplat „{parkingSpot}” ist bereits vergeben!")
        return False
    db = get_db()
    try:
        bookings = db.execute(
                "INSERT INTO booking (username, startRange, endRange, parkingspot) VALUES (?,?,?,?)",
                (username, startRange, endRange, parkingSpot),
                )
        bookings.commit()
        return True
    except db.IntegrityError:
        flash(f"Buchung konnte nicht durchgeführt werden!")
        return False
    else:
        flash(f"Buchung erfolgreich.")
        return True
    
    return True