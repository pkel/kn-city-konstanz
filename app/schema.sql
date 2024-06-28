
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

DROP TABLE IF EXISTS booking;

CREATE TABLE booking (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  startRange TEXT NOT NULL,
  endRange TEXT NOT NULL,
  parkingSpot TEXT NOT NULL
);

INSERT INTO booking (id,username, startRange, endRange, parkingSpot) VALUES
(1, "a", "2024-06-28", "2024-06-30","test"),
(2, "b", "2024-06-28", "2024-06-30","test2");
