const Calendar = tui.Calendar;

const calendar = new Calendar("#calendar", {
  defaultView: "week",
  week: {
    taskView: false,
    eventView: ["time"],
    showAllDay: false
  },
  useFormPopup: true,
  useDetailPopup: true

});


// from, to, isMine
fakeEvents = [
  ["2024-06-29T09:00:00", "2024-06-29T10:00:00", false],
  ["2024-06-29T12:00:00", "2024-06-29T14:00:00", true],
  ["2024-06-29T15:00:00", "2024-06-29T16:00:00", false],
]

fakeEvents.forEach(event => {
  calendar.createEvents([{
    title: event[2] ? "My Event" : "Other Event",
    body: "Fake Event",
    start: event[0],
    end: event[1],
    backgroundColor: event[2] ? "#22aa22" : "#cccccc",
    isReadOnly: !event[2],
  }]);

  calendar.clearGridSelections();
});

// ... GET would be at start ... //

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
}



/* --------------------------------- Events --------------------------------- */
calendar.on('beforeCreateEvent', (eventObj) => {

  // ... validate here ...

  if (!clientsideValidate(eventObj)) {
    console.log("kke");
    calendar.clearGridSelections();
    return;
  }

  calendar.createEvents([{
    isReadOnly: true,
    isPrivate: true,
    ...eventObj
  }]);

  
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