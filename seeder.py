#!/usr/bin/python

from application.database import db

USERS = [
    ['Steve'],
    ['Bob'],
    ['Mike'],
]

CATS = [
    ['Tibbles', 'Steve'],
    ['Ginger', None],
    ['Meow', 'Steve'],
    ['Tabby', 'Mike'],
]

INSERT_USER_SQL = f"insert into user(name) values {', '.join('%s' for user in USERS)}"

INSERT_CAT_SQL = f"insert into cat (name, owner_id) " \
                 f"(select ins.cat_name as name, " \
                 f"user.id as owner_id " \
                 f"from (values " \
                 f"{', '.join('row%s' for cat in CATS)}" \
                 f") as ins(cat_name, owner_name) " \
                 f"left join user on ins.owner_name = user.name)"


def seed(sql_query, arguments, debug=False):
    with db.cursor() as cursor:
        if debug:
            print(cursor.mogrify(sql_query, arguments))
        cursor.execute(sql_query, arguments)
        db.commit()


seed(INSERT_USER_SQL, USERS)
seed(INSERT_CAT_SQL, CATS)
print('Database seeded successfully!')
