from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/profile')
def profile():
    username = g.user["username"]
    weight = g.user["weight"]
    height = g.user["height"] / 100
    bmi = round(weight/height/height)
    
    return render_template('blog/profile.html', username=username, bmi=bmi)

@bp.route('/menu', methods=('GET', 'POST'))
def menu():
    bmi = request.args.get("bmi")
    eat_time = request.args.get("eat_time")
    
    db = get_db()
    menus = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE eattime = ?',
        (eat_time,)
    ).fetchall()

    id = 1
    return render_template('blog/order.html', eat_time=eat_time, id=id, menus=menus)


@bp.route('/morning')
def morning():
    db = get_db()
    menus = db.execute(
        'SELECT *'
        ' FROM menu'
    ).fetchall()

    eat_time = "朝"
    username = g.user["username"]
    weight = 60
    height = 170 / 100
    bmi = weight/height/height
    id = 1
    return render_template('blog/order.html', eat_time=eat_time, id=id, menus=menus)

@bp.route('/lunch')
def lunch():
    eat_time = "昼"
    username = g.user["username"]
    weight = 60
    height = 170 / 100
    bmi = weight / height / height
    id = 1
    
    return render_template('blog/order.html', eat_time=eat_time, id=id)

@bp.route('/dinner')
def dinner():
    eat_time = "晩"
    username = g.user["username"]
    weight = 60
    height = 170 / 100
    bmi = weight / height / height
    id = 1
    
    return render_template('blog/order.html', eat_time=eat_time, id=id)

@bp.route('/detail', methods=('GET', 'POST'))
def detail():
    # id = request.args.get("id")
    id = request.args.get("id")
    return render_template('blog/detail.html', id=id)

@bp.route('/profile/<int:id>', methods=('GET', 'POST'))
def ordered(id):
    # orderテーブルに挿入する
    username = g.user["username"]
    weight = 60
    height = 170 / 100
    bmi = weight/height/height
    print("log")
    return render_template('blog/profile.html', id=id, username=username, bmi=bmi)

@bp.route('/log', methods=('GET', 'POST'))
def log():
    return render_template('blog/log.html')

@bp.route('/')
def index():
    # print("test{}".format(g.user['id']))
    db = get_db()
    try:
        posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.author_id = ?'
            ' ORDER BY created DESC',
            (g.user['id'],)
        ).fetchall()
    except:
        posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
        ).fetchall()
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' WHERE p.author_id = ?'
    #     ' ORDER BY created DESC',
    #     (g.user['id'],)
    # ).fetchall()
    return render_template('blog/top.html', posts=posts)

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