DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS ordered;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  address TEXT,
  weight INTEGER,
  height INTEGER,
  gender TEXT,
  course TEXT
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- created DATE DEFAULT (datetime('now')),
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE menu (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  menuname TEXT UNIQUE NOT NULL,
  img TEXT NOT NULL,
  eattime TEXT NOT NULL,
  type TEXT NOT NULL,
  calorie INTEGER NOT NULL,
  details TEXT NOT NULL
);

CREATE TABLE ordered (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  menuid INTEGER NOT NULL,
  userid INTEGER NOT NULL,
  menuname TEXT NOT NULL,
  img TEXT NOT NULL,
  eattime TEXT NOT NULL,
  type TEXT NOT NULL,
  calorie INTEGER NOT NULL,
  details TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (userid) REFERENCES user (id)
);


insert into menu values(1, "納豆的食1", "health_01.png", "morning", "low", 100, "説明文1");
insert into menu values(2, "納豆的食2", "health_02.png", "morning", "low", 200, "説明文2");
insert into menu values(3, "納豆的食3", "health_03.png", "morning", "low", 300, "説明文3");
insert into menu values(4, "納豆的食4", "health_04.png", "lunch", "low", 400, "説明文4");
insert into menu values(5, "納豆的食5", "health_05.png", "lunch", "low", 500, "説明文5");
insert into menu values(6, "納豆的食6", "health_06.png", "lunch", "low", 600, "説明文6");
insert into menu values(7, "納豆的食7", "health_07.png", "dinner", "low", 700, "説明文7");
insert into menu values(8, "納豆的食8", "health_08.png", "dinner", "low", 800, "説明文8");
insert into menu values(9, "納豆的食9", "health_09.png", "dinner", "low", 900, "説明文9");
insert into menu values(10, "納豆的食10", "health_10.png", "morning", "high", 1000, "説明文10");
insert into menu values(12, "納豆的食12", "health_12.png", "morning", "high", 1200, "説明文12");
insert into menu values(13, "納豆的食13", "health_13.png", "morning", "high", 1300, "説明文13");
insert into menu values(14, "納豆的食14", "health_14.png", "lunch", "high", 1400, "説明文14");
insert into menu values(15, "納豆的食15", "health_15.png", "lunch", "high", 1500, "説明文15");
insert into menu values(16, "納豆的食16", "health_16.png", "lunch", "high", 1600, "説明文16");
insert into menu values(17, "納豆的食17", "health_17.png", "dinner", "high", 1700, "説明文17");
insert into menu values(18, "納豆的食18", "health_18.png", "dinner", "high", 1800, "説明文18");
insert into menu values(19, "納豆的食19", "health_19.png", "dinner", "high", 1900, "説明文19");