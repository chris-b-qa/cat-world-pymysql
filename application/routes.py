#!/usr/bin/python

from application import app, db
from application.forms import UserForm, CatForm, DeleteForm, EditForm
from flask import flash, render_template, redirect, abort, session, request
from werkzeug.datastructures import MultiDict

CAT_FORM_DATA = 'cat_form'
USER_FORM_DATA = 'user_form'
# ---------------------- User routes ----------------------


@app.route('/users')
def get_users():
    with db.cursor() as cursor:
        sql = "select * from user"
        cursor.execute(sql)
        users = cursor.fetchall()
        return render_template("/users.html", users=users)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    user_sql = "select * from user where id = %s"
    user_cats_sql = "select * from cat where owner_id = %s"

    with db.cursor() as cursor:
        cursor.execute(user_sql, user_id)
        user = cursor.fetchone()

        cursor.execute(user_cats_sql, user_id)
        user['cats'] = cursor.fetchall()

        if user is None:
            abort(404)

        edit_form = EditForm()
        delete_form = DeleteForm()
        return render_template('user.html', user=user, edit_form=edit_form, delete_form=delete_form)


@app.route('/users', methods=['POST'])
def create_user():
    user_form = UserForm()

    if user_form.validate():
        new_user_sql = 'insert into user(name) values (%s)'
        name = user_form.name.data

        with db.cursor() as cursor:
            cursor.execute(new_user_sql, name)
            db.commit()

            if cursor.rowcount != 1:
                abort(409)

        flash(f'{name} added successfully!')
        return redirect('/')

    session[USER_FORM_DATA] = request.form
    return redirect('/')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    name_sql = 'select name from user where id = %s'
    orphan_cats_sql = 'update cat set owner_id = null where owner_id = %s'
    delete_sql = 'delete from user where id = %s'

    with db.cursor() as cursor:
        cursor.execute(name_sql, user_id)
        name = cursor.fetchone()['name'] if cursor.rowcount == 1 else 'User'

        cursor.execute(orphan_cats_sql, user_id)
        cursor.execute(delete_sql, user_id)
        db.commit()

    flash(f'{name} has been deleted!')
    return redirect('/')


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    edit_form = EditForm()

    if edit_form.validate():
        name = edit_form.name.data
        edit_user_sql = 'update user set name=%s where id=%s'

        with db.cursor() as cursor:
            cursor.execute(edit_user_sql, (name, user_id))
            db.commit()

            if cursor.rowcount != 1:
                abort(404)

        flash(f'{name} has been updated!')
        return redirect(f'/users/{ user_id }')

    return abort(400)

# # ---------------------- Cat routes ----------------------


@app.route('/cats')
def get_cats():
    cats_sql = 'select cat.id, cat.name, user.name as owner_name from cat left join user on cat.owner_id=user.id'

    with db.cursor() as cursor:
        cursor.execute(cats_sql)
        cats = cursor.fetchall()

    return render_template("/cats.html", cats=cats)


@app.route('/cats/<int:cat_id>')
def get_cat(cat_id):
    cat_sql = 'select * from cat where id = %s'
    cat_owner_sql = 'select user.id, user.name from cat inner join user on user.id=cat.owner_id where cat.id = %s'

    delete_form = DeleteForm()
    edit_form = EditForm()

    with db.cursor() as cursor:
        cursor.execute(cat_sql, cat_id)

        if cursor.rowcount != 1:
            abort(404)

        cat = cursor.fetchone()

        cursor.execute(cat_owner_sql, cat_id)
        cat['owner'] = cursor.fetchone()

    return render_template('cat.html', cat=cat, edit_form=edit_form, delete_form=delete_form)


@app.route('/cats', methods=['POST'])
def create_cat():
    cat_form = CatForm()
    cat_form.update_owners()

    if cat_form.validate():
        create_cat_sql = 'insert into cat (name, owner_id) values (%s, %s)'
        name = cat_form.name.data
        owner_id = cat_form.owner_id.data

        with db.cursor() as cursor:
            cursor.execute(create_cat_sql, (name, owner_id))
            db.commit()

            if cursor.rowcount != 1:
                abort(409)

        flash(f'{name} added successfully!')

    session[CAT_FORM_DATA] = request.form
    return redirect('/')


@app.route('/cats/<int:cat_id>/delete', methods=['POST'])
def delete_cat(cat_id):
    name_sql = 'select name from cat where id = %s'
    delete_sql = 'delete from cat where id = %s'

    with db.cursor() as cursor:
        cursor.execute(name_sql, cat_id)
        name = cursor.fetchone()['name'] if cursor.rowcount == 1 else 'Cat'
        cursor.execute(delete_sql, cat_id)
        db.commit()

    flash(f'{name} has been deleted!')
    return redirect('/')


@app.route('/cats/<int:cat_id>/edit', methods=['POST'])
def edit_cat(cat_id):
    edit_form = EditForm()

    if edit_form.validate():
        name = edit_form.name.data
        edit_cat_sql = 'update cat set name=%s where id=%s'

        with db.cursor() as cursor:
            cursor.execute(edit_cat_sql, (name, cat_id))
            db.commit()

            if cursor.rowcount != 1:
                abort(404)

        flash(f'{name} has been updated!')
        return redirect(f'/cats/{ cat_id }')

    return abort(400)


@app.route('/')
def index():
    with db.cursor() as cursor:
        users_count_sql = 'select count(id) as user_count from user'
        cursor.execute(users_count_sql)
        users_count = cursor.fetchone()['user_count']

        cats_count_sql = 'select count(id) as cat_count from cat'
        cursor.execute(cats_count_sql)
        cats_count = cursor.fetchone()['cat_count']

    cat_form_data = session.get(CAT_FORM_DATA)
    cat_form = CatForm(MultiDict(cat_form_data))
    cat_form.update_owners()

    if cat_form_data is not None:
        session.pop(CAT_FORM_DATA)
        cat_form.validate()

    user_form_data = session.get(USER_FORM_DATA)
    user_form = UserForm(MultiDict(user_form_data))

    if user_form_data is not None:
        session.pop(USER_FORM_DATA)
        user_form.validate()

    return render_template('index.html', user_form=user_form, cat_form=cat_form, users_count=users_count,
                           cats_count=cats_count)
