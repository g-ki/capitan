drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text unique not null,
  password text not null
);

drop table if exists keys;
create table keys (
  id integer primary key autoincrement,
  key text not null,
  user_id integer not null
);
