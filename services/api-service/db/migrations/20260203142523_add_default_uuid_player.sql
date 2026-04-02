-- migrate:up
alter table players alter column id set default uuidv7();

-- migrate:down
alter table players alter column id drop default;
