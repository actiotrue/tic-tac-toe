-- migrate:up
alter table players
add column created_at timestamp default current_timestamp,
add column updated_at timestamp default current_timestamp;

create or replace function update_timestamp()
returns trigger as $$
begin
    new.updated_at = current_timestamp;
    return new;
end;
$$ language 'plpgsql';

create trigger set_timestamp
before update on players
for each row 
execute function update_timestamp(); 

-- migrate:down
alter table players
drop column created_at,
drop column updated_at;

drop trigger if exist set_timestamp on players;