-- migrate:up
create type game_result as enum ('x_won','o_won','draw');
create table games (
    id uuid primary key,
    player_x_id uuid references players(user_id) on delete cascade,
    player_o_id uuid references players(user_id) on delete cascade,
    result game_result,
    duration int not null,
    created_at timestamp default current_timestamp
);


-- migrate:down
drop table games;
drop type game_result;