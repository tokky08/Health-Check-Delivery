from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/profile/<int:user_id>')
def profile(user_id):
    user = user_get(user_id)
    username = user["username"]
    bmi = bmi_get(user)
    
    return render_template('blog/profile.html', username=username, bmi=bmi, user_id=user_id)

@bp.route('/menu/<int:user_id>/<int:bmi>', methods=('GET', 'POST'))
def menu(user_id, bmi):
    type_bmi = "low" if bmi < 25 else "high"
    eat_time = request.args.get("eat_time")

    db = get_db()
    menus = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE eattime = ? and type = ?',
        (eat_time, type_bmi,)
    ).fetchall()

    return render_template('blog/order.html', eat_time=eat_time, menus=menus, user_id=user_id)

@bp.route('/detail/<int:user_id>', methods=('GET', 'POST'))
def detail(user_id):
    menu_id = request.args.get("menu_id")
    db = get_db()
    menu = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE id = ?',
        (menu_id,)
    ).fetchone()
    return render_template('blog/detail.html', user_id=user_id, menu_id=menu_id, menu=menu)

@bp.route('/profile/<int:user_id>/<int:menu_id>', methods=('GET', 'POST'))
def ordered(user_id, menu_id):
    user = user_get(user_id)
    username = user["username"]
    bmi = bmi_get(user)

    db = get_db()
    menu = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE id = ?',
        (menu_id,)
    ).fetchone()

    menuname = menu["menuname"]
    img = menu["img"]
    eattime = menu["eattime"]
    type_bmi = menu["type"]
    calorie = menu["calorie"]
    details = menu["details"]
    
    db.execute(
        'INSERT INTO ordered (menuid, userid, menuname, img, eattime, type, calorie, details)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (menu_id, user_id, menuname, img, eattime, type_bmi, calorie, details)
    )
    db.commit()
    
    return render_template('blog/profile.html', user_id=user_id, menu_id=menu_id, username=username, bmi=bmi)

@bp.route('/log/<int:user_id>', methods=('GET', 'POST'))
def log(user_id):
    db = get_db()
    logs = db.execute(
        'SELECT *'
        ' FROM ordered o JOIN user u ON o.userid = u.id'
        ' WHERE o.userid = ?'
        ' ORDER BY created DESC',
        (user_id,)
    ).fetchall()
    
    return render_template('blog/log.html', logs=logs)

@bp.route('/')
def index():
    return render_template('blog/top.html')

def user_get(user_id):
    db = get_db()
    user = db.execute(
        'SELECT *'
        ' FROM user'
        ' WHERE id = ?',
        (user_id,)
    ).fetchone()

    return user

def bmi_get(user):
    weight = user["weight"]
    height = user["height"] / 100
    bmi = round(weight / height / height)
    
    return bmi






@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))