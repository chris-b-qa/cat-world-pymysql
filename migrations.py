#!/usr/bin/python

from application.database import db

USER_TABLE_SQL = "create table if not exists user (" \
                "id int auto_increment primary key," \
                "name varchar(255) not null," \
                "created_at timestamp not null default now()," \
                "updated_at timestamp not null default now() on update now()" \
                ")"

CAT_TABLE_SQL = "create table if not exists cat (" \
                "id int auto_increment primary key," \
                "name varchar(255) not null," \
                "owner_id int," \
                "created_at timestamp not null default now()," \
                "updated_at timestamp not null default now() on update now()," \
                "foreign key (owner_id) references user (id)" \
                ")"

with db.cursor() as cursor:
    cursor.execute(USER_TABLE_SQL)
    cursor.execute(CAT_TABLE_SQL)
    db.commit()

print('All migrations ran successfully!')
