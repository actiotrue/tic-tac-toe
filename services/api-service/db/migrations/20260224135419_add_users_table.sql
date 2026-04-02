-- migrate:up
create table users (
    id uuid primary key,
    hashed_password varchar(255) not null,
    username varchar(255) not null
);

alter table players drop column hashed_password;
alter table players drop column id;
alter table players add column user_id uuid primary key references users(id) on delete cascade; 

-- migrate:down
drop table users;
alter table players add column hashed_password varchar(255) not null;
alter table players add column id uuid primary key;
alter table players drop column user_id;