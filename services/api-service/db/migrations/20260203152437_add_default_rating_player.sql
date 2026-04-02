-- migrate:up
alter table players alter column rating set default 1000;

-- migrate:down
alter table players alter column rating drop default;

