from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from app.db import get_db
from app.auth import login_required
from datetime import datetime

from . import map

blueprint = Blueprint('booking', __name__, url_prefix=None)

# Filter for parking slot
def filterBooking(forName=None):
    selectStatement = "SELECT id, companyId, startDateTime, endDateTime FROM booking"
    if forName is None:
        return (selectStatement,
                ())
    else:
        return (selectStatement + " WHERE zone = ?",
                (forName,))

# Query for a list of bookings for parking slots with filter applied
def searchBooking(filter):
    db = get_db()
    try:
        return db.execute(filter[0], filter[1]).fetchall()
    except db.IntegrityError:
        flash(f"Unbekannter Parkplatz „{zone}” erkannt!")
        return []

@blueprint.get('/reservieren/zone/<int:zone_id>/bookings')
@login_required
def getBookings(zone_id):
    companyId = g.user["id"]
    zone = map.zone(zone_id)

    bookings = searchBooking(filterBooking(forName=zone))
    if bookings is None:
        flash(f"Keine Buchungen gefunden!")
        return []

    bookingList = [{
        "id": each["id"],
        "isMine": True if companyId == each["companyId"] else False,
        "startDateTime": each["startDateTime"],
        "endDateTime": each["endDateTime"]
    } for each in bookings]

    return jsonify(bookingList)

def alreadyBooked(zone, startDateTime, endDateTime):
    bookings = searchBooking(filterBooking(forName=zone))
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

@blueprint.get('/reservieren')
@login_required
def getUserBooking():
    companyId = g.user["id"]
    db = get_db()
    try:
        bookings = db.execute(
                "SELECT id, companyId, startDateTime, endDateTime FROM booking WHERE companyId = ?",
                (companyId,),
                ).fetchall()
    except db.IntegrityError:
        flash(f"Buchung konnte geholt werden!")
        return "internal error", 404
    else:
        bookingList = ([{
        "id": each["id"],
        "startDateTime": each["startDateTime"],
        "endDateTime": each["endDateTime"]
            } for each in bookings])
    if len(bookingList) == 0:
        flash(f"Keine Buchung vorhanden! Bitte Reservierung vornehmen.")
    return render_template('mybookings.html', bookingList=bookingList)

@blueprint.delete('/reservieren/<int:booking_id>')
@login_required
def deleteUserBooking(booking_id):
    companyId = g.user["id"]

    db = get_db()
    try:
        db.execute(
                "DELETE booking WHERE id = ? and companyId = ?",
                (booking_id, companyId),
                )
        db.commit()
    except db.IntegrityError:
        flash(f"Buchung konnte nicht gelöscht werden!")
        return {
            "canDelete": False,
            "cause": "internal error"
        }
    else:
        flash(f"Buchung erfolgreich gelöscht.")
        return {
            "canDelete": True
        }

@blueprint.put('/reservieren/<int:booking_id>')
@login_required
def updateUserBooking(booking_id):
    companyId = g.user["id"]
    startDateTime = request.form['startDateTime']
    endDateTime = request.form['endDateTime']
    db = get_db()
    try:
        db.execute(
                "UPDATE booking SET startDateTime=? endDateTime=? zone=? WHERE id = ?",
                (startDateTime, endDateTime, zone, booking_id),
                )
        db.commit()
    except db.IntegrityError:
        flash(f"Buchung konnte nicht verändert werden!")
        return {
            "canBook": False,
            "cause": "internal error"
        }
    else:
        flash(f"Buchung erfolgreich.")
        return {
            "canBook": True
        }

@blueprint.post('/reservieren/zone/<int:zone_id>')
@login_required
def book(zone_id):
    companyId = g.user["id"]
    startDateTime = request.form['startDateTime']
    endDateTime = request.form['endDateTime']

    zone = map.zone(zone_id)

    if alreadyBooked(zone, startDateTime, endDateTime):
        flash(f"Der Parkplat „{zone}” ist bereits vergeben!")
        return {
            "canBook": False,
            "cause": "already booked"
        }
    db = get_db()
    try:
        db.execute(
                "INSERT INTO booking (companyId, startDateTime, endDateTime, zone) VALUES (?,?,?,?)",
                (companyId, startDateTime, endDateTime, zone),
                )
        db.commit()
    except db.IntegrityError:
        flash(f"Buchung konnte nicht durchgeführt werden!")
        return {
            "canBook": False,
            "cause": "internal error"
        }
    else:
        flash(f"Buchung erfolgreich.")
        return {
            "canBook": True
        }

@blueprint.get('/reservieren/zone/<int:zone_id>')
@login_required
def form(zone_id):
    zone = map.zone(zone_id)
    return render_template('reserve.html', zone=zone)
