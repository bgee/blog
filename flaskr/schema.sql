drop table if exists entries;
drop table if exists comments;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);
create table comments (
  comment_id integer primary key autoincrement,
  commenter text not null,
  text text not null,
  entry_id integer,
  FOREIGN KEY(entry_id) REFERENCES entries(id)
);
