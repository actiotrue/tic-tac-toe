-- migrate:up
alter table players add column image_url varchar(255) not null;

-- migrate:down
alter table players drop column image_url; 
