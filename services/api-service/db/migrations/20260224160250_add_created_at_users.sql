-- migrate:up
alter table users
add column created_at timestamp default current_timestamp,
add column updated_at timestamp default current_timestamp;

create trigger set_timestamp
before update on users
for each row 
execute function update_timestamp(); 

-- migrate:down
alter table users
drop column created_at,
drop column updated_at;

drop trigger if exists set_timestamp() on users;
