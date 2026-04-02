-- migrate:up
alter table players alter column wins set default 0;
alter table players alter column losses set default 0;
alter table players alter column draws set default 0;

-- migrate:down
alter table players alter column wins drop default;
alter table players alter column losses drop default;
alter table players alter column draws drop default;
