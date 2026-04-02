-- migrate:up
alter table games add column winner_id uuid;

-- migrate:down
alter table games drop column winner_id;