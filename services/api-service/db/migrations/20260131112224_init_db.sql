-- migrate:up
create table players (
    id uuid primary key,
    hashed_password varchar(255) not null,
    username varchar(255) not null,
    rating int not null,
    wins int not null,
    draws int not null,
    losses int not null
);

-- migrate:down
drop table players;
