-- migrate:up
create type player_type as enum ('human','ai');

create table game_players (
    id uuid primary key default gen_random_uuid(),
    game_id uuid references games(id) on delete cascade,
    player_id uuid references players(user_id) on delete cascade,
    side varchar(20) not null,
    type player_type not null,
    created_at timestamp default current_timestamp,

    unique (game_id, side) 
);

alter table games drop column player_x_id;
alter table games drop column player_o_id;
alter table games drop column winner_id;

-- migrate:down
alter table games add column player_o_id uuid;
alter table games add constraint games_player_o_id_fkey foreign key (player_o_id) references players(user_id) on delete cascade;

alter table games add column player_x_id uuid;
alter table games add constraint games_player_x_id_fkey foreign key (player_x_id) references players(user_id) on delete cascade;

alter table games add column winner_id uuid;

drop table if exists game_players;
drop type if exists player_type;
