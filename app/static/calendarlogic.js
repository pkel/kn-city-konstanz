const Calendar = tui.Calendar;
function generateUUID() { // Public Domain/MIT
  var d = new Date().getTime();//Timestamp
  var d2 = ((typeof performance !== 'undefined') && performance.now && (performance.now()*1000)) || 0;//Time in microseconds since page-load or 0 if unsupported
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16;//random number between 0 and 16
      if(d > 0){//Use timestamp until depleted
          r = (d + r)%16 | 0;
          d = Math.floor(d/16);
      } else {//Use microseconds since page-load if supported
          r = (d2 + r)%16 | 0;
          d2 = Math.floor(d2/16);
      }
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

const calendar = new Calendar("#calendar", {
  defaultView: "week",
  week: {
    taskView: false,
    eventView: ["time"],
    showAllDay: false,
    dayNames: ["Son", "Mon", "Die", "Mit", "Don", "Fre", "Sam"],
    startDayOfWeek: 1

  },
  useFormPopup: true,
  useDetailPopup: true

});

const allEventsState = []; // calendar itself does not store events, so we need to keep track of them

// from, to, isMine
fakeEvents = [
  ["2024-06-29T09:00:00", "2024-06-29T10:23:00", false],
  ["2024-06-29T12:00:00", "2024-06-29T14:43:00", true],
  ["2024-06-29T15:07:00", "2024-06-29T16:53:00", false],
]

function createBookingEvent(start, end, isMine) {
  const id = generateUUID();
  start = new Date(start);
  end = new Date(end);
  console.log("Creating event", id, start, end, isMine)
  allEventsState.push({id: id, start: start, end: end, isMine: isMine});

  calendar.createEvents([{
    id: id,
    title: isMine ? "": "Booked",
    start: start,
    end: end,
    backgroundColor: isMine ? "#22aa22" : "#cccccc",
    isReadOnly: !isMine,
  }]);
}

fakeEvents.forEach(event => {
  createBookingEvent(event[0], event[1], event[2]);
  calendar.clearGridSelections();
});

function populateCalendar(zoneId) {
  // Get events from server // filler for now
  fetch("/reservieren/zone/"+zoneId+"/bookings")
    .then(response => response.json())
    .then(data => {
      data.forEach(event => {

        createBookingEvent(event.startDateTime, event.endDateTime, event.isMine);
      });
    });
}

function clientsideValidate(eventObj) {
  eventObj.start = new Date(eventObj.start);
  eventObj.end = new Date(eventObj.end);

  // must be min 30 mins and max 4 hrs and positive
  if (eventObj.end - eventObj.start < 30 * 60 * 1000 || eventObj.end - eventObj.start > 4 * 60 * 60 * 1000) {
    alert("Event must be between 30 mins and 4 hours");
    return false;
  }

  // must be in future
  if (eventObj.start < new Date()) {
    alert("Event must be in the future");
    return false;
  }

  // must not overlap with other events
  for (let i = 0; i < allEventsState.length; i++) {
    let otherEvent = allEventsState[i];
    if (otherEvent.id === eventObj.id) continue; // skip self (if updating event

    otherEvent.start = new Date(otherEvent.start);
    otherEvent.end = new Date(otherEvent.end);
    if (eventObj.start < otherEvent.end && eventObj.end > otherEvent.start) {
      console.log(eventObj, otherEvent);
      alert("Event must not overlap with other events");
      return false;
    }
  }

  return true;
}


function postBooking(start, end) {
  fetch("/bookings", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      start: start,
      end: end
    }),
  });
}


/* --------------------------------- Events --------------------------------- */
calendar.on('beforeCreateEvent', (eventObj) => {

  // ... validate here ...

  if (!clientsideValidate(eventObj)) {
    calendar.clearGridSelections();
    return;
  }


  // send to server
  postBooking(eventObj.start, eventObj.end);

  createBookingEvent(eventObj.start, eventObj.end, true);

  calendar.clearGridSelections();
});


calendar.on("beforeUpdateEvent", (updatedEvent) => {
  let oldEvent = updatedEvent.event;
  let changes = updatedEvent.changes;

  let newEvent = {
    ...oldEvent,
    ...changes
  };

  if (!clientsideValidate(newEvent)) {
    return;
  }

  // send to server
  postBooking(newEvent.start, newEvent.end);
  console.log(oldEvent, "Updated to", newEvent);
  console.log("Updated event", oldEvent.id, changes);

  calendar.updateEvent(oldEvent.id, "", changes);

});


/* -------------------------------- Nav Btns -------------------------------- */
const btnNext = document.getElementById("btnNext");
btnNext.addEventListener("click", function() {
  calendar.next();
});

const btnPrev = document.getElementById("btnPrev");
btnPrev.addEventListener("click", function() {
  calendar.prev();
});

const btnToday = document.getElementById("btnToday");
btnToday.addEventListener("click", function() {
  calendar.today();
});