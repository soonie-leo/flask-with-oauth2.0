DROP TABLE IF EXISTS logo;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS banner;
DROP TABLE IF EXISTS history;

CREATE TABLE logo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  img_link TEXT NOT NULL
);

CREATE TABLE menu (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  link TEXT NOT NULL,
  num INTEGER NOT NULL
);

CREATE TABLE banner (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  img_link TEXT NOT NULL,
  external_link TEXT NOT NULL,
  num INTEGER NOT NULL
);

CREATE TABLE history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  method TEXT NOT NULL DEFAULT "",
  data TEXT NOT NULL DEFAULT ""
);