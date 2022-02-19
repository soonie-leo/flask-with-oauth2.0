DROP TABLE IF EXISTS store;
DROP TABLE IF EXISTS logo;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS banner;
DROP TABLE IF EXISTS image;

CREATE TABLE store (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  access_token TEXT NOT NULL,
  access_token_expire TIMESTAMP NOT NULL,
  refresh_token TEXT NOT NULL,
  refresh_token_expire TIMESTAMP NOT NULL
);
INSERT INTO store (access_token, access_token_expire, refresh_token, refresh_token_expire) VALUES ("Coo1kQHHO5viWTCdc4qfRC", "2022-02-19 16:43:07", "IXtcmpckCRVlyZmyRKHV2C", "2022-03-05 14:43:07");

CREATE TABLE logo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  img_link TEXT NOT NULL
);
INSERT INTO logo (img_link) VALUES ("https://{mall_id}.com/lib/images/logo_001.png");

CREATE TABLE menu (
  id INTEGER PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  link TEXT NOT NULL
);
INSERT INTO menu (id, title, link) VALUES (1, "메뉴명1", "/index.html");
INSERT INTO menu (id, title, link) VALUES (2, "메뉴명2", "/member/login.html");
INSERT INTO menu (id, title, link) VALUES (3, "", "");
INSERT INTO menu (id, title, link) VALUES (4, "", "");

CREATE TABLE banner (
  id INTEGER PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  img_link TEXT NOT NULL,
  external_link TEXT NOT NULL,
  activate INTEGER NOT NULL DEFAULT 0
);
INSERT INTO banner (id, img_link, external_link, activate) VALUES (1, "https://{mall_id}.cafe24.com/lib/main/top1/210900/bg.jpg", "/index.html", 1);
INSERT INTO banner (id, img_link, external_link, activate) VALUES (2, "https://{mall_id}.cafe24.com/lib/main/top1/210900/bg.jpg", "/index.html", 1);
INSERT INTO banner (id, img_link, external_link, activate) VALUES (3, "", "", 0);
INSERT INTO banner (id, img_link, external_link, activate) VALUES (4, "", "", 0);

CREATE TABLE image (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  path TEXT NOT NULL
);
INSERT INTO image (path) VALUES ("https://{mall_id}.cafe24.com/lib/images/logo_001.png");
INSERT INTO image (path) VALUES ("https://{mall_id}.cafe24.com/web/upload/NNEditor/20220219/ed16b2ae7c431346b4c205f476d1b9e0.png");
