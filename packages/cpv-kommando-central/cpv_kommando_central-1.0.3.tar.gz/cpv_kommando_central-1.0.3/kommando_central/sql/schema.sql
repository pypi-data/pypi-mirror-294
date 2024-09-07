DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS commands;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS departments;

CREATE TABLE roles (
  id TEXT PRIMARY KEY
);

CREATE TABLE departments (
  id TEXT PRIMARY KEY,
  department_name TEXT UNIQUE NOT NULL
);

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role_id TEXT,
  department_id INTEGER NOT NULL,
  FOREIGN KEY(role_id) REFERENCES roles(id),
  FOREIGN KEY(department_id) REFERENCES departments(id)
);

CREATE TABLE commands (
  id TEXT PRIMARY KEY,
  command_name TEXT NOT NULL
);

CREATE TABLE tracks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  department_id INTEGER NOT NULL,
  track_name TEXT NOT NULL,
  description TEXT,
  FOREIGN KEY(department_id) REFERENCES departments(id)
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  from_track_id INTEGER NOT NULL,
  to_track_id INTEGER NOT NULL,
  command_id TEXT NOT NULL,
  message TEXT,
  FOREIGN KEY(from_track_id) REFERENCES tracks(id),
  FOREIGN KEY(to_track_id) REFERENCES tracks(id)
  FOREIGN KEY(command_id) REFERENCES commands(id)
);
