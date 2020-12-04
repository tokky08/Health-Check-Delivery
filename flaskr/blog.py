from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    return render_template('blog/top.html')

@bp.route('/<user_name>/profile', methods=('GET', 'POST'))
def profile(user_name):
    user = user_get(user_name)
    bmi = bmi_get(user)
    menu_id = request.args.get("menu_id")

    db = get_db()
    gender = db.execute(
        'SELECT gender'
        ' FROM user'
        ' WHERE username = ?',
        (user_name,)
    ).fetchone()

    if gender == "male":
        img_gender = "male"
    else:
        img_gender = "female"

    if bmi < 20:
        img_type = "slim"
        type_bmi = "低体重タイプ"
        type_disc = "あなたは痩せ気味のため、毎日３食しっかり摂取し、適正体重の維持とバランスのとれた食生活の確立を目指しましょう。"
    elif 25 < bmi:
        img_type = "plump"
        type_bmi = "肥満タイプ"
        type_disc = "あなたは肥満気味のため、野菜やキノコ類、海藻類など栄養豊富なものを摂取し、規則正しい食事を送ることを心がけましょう。"
    else:
        img_type = "standard"
        type_bmi = "標準タイプ"
        type_disc = "あなたは健康的な体です。このままの状態を維持し、毎日健康的な食生活を送りましょう。"

    if menu_id:
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
            'INSERT INTO ordered (menuid, username, menuname, img, eattime, type, calorie, details)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (menu_id, user_name, menuname, img, eattime, type_bmi, calorie, details)
        )
        db.commit()
        
    return render_template('blog/profile.html',
        user_name=user_name,
        bmi=bmi,
        type_bmi = type_bmi,
        type_disc=type_disc,
        img_gender=img_gender,
        img_type = img_type
    )

@bp.route('/<user_name>/check', methods=('GET', 'POST'))
def check(user_name):
    menu_id = request.args.get("menu_id")
    if menu_id:
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



@bp.route('/<user_name>/menu/<int:bmi>', methods=('GET', 'POST'))
def menu(user_name, bmi):
    type_bmi = "low" if bmi < 25 else "high"
    eat_time = request.args.get("eat_time")

    db = get_db()
    menus = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE eattime = ? and type = ?',
        (eat_time, type_bmi,)
    ).fetchall()

    return render_template('blog/order.html', eat_time=eat_time, menus=menus, user_name=user_name)

@bp.route('/<user_name>/detail', methods=('GET', 'POST'))
def detail(user_name):
    menu_id = request.args.get("menu_id")
    db = get_db()
    menu = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE id = ?',
        (menu_id,)
    ).fetchone()
    return render_template('blog/detail.html', user_name=user_name, menu_id=menu_id, menu=menu)


@bp.route('/<user_name>/log', methods=('GET', 'POST'))
def log(user_name):
    db = get_db()
    logs = db.execute(
        'SELECT *'
        ' FROM ordered o JOIN user u ON o.username = u.username'
        ' WHERE o.username = ?'
        ' ORDER BY created DESC',
        (user_name,)
    ).fetchall()
    
    return render_template('blog/log.html', logs=logs)

@bp.route('/<user_name>/update', methods=('GET', 'POST'))
# @login_required
def update_1(user_name):
    user = user_get(user_name)

    if request.method == 'POST':
        address = request.form['address']
        tel = request.form["tel"]
        mail = request.form["mail"]
        weight = request.form['weight']
        height = request.form['height']
        gender = request.form['gender']
        allergies = request.form.getlist('allergies')
        error = None

        egg = 0
        milk = 0
        wheat = 0
        shrimp = 0
        crab = 0
        peanuts = 0
        soba = 0
        for item in allergies:
            if item == "egg":
                egg = 1
            elif item == "milk":
                milk = 1
            elif item == "wheat":
                wheat = 1
            elif item == "shrimp":
                shrimp = 1
            elif item == "crab":
                crab = 1
            elif item == "peanuts":
                peanuts = 1
            elif item == "soba":
                soba = 1

        # if not title:
        #     error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET address = ?, tel = ?, mail = ?, weight = ?, height = ?, gender = ?, egg = ?, milk = ?, wheat = ?, shrimp = ?, crab = ?, peanuts = ?, soba = ?'
                ' WHERE username = ?',
                (address, tel, mail, weight, height, gender, egg, milk, wheat, shrimp, crab, peanuts, soba, user_name)
            )
            db.commit()
            return redirect(url_for('blog.profile', user_name=user_name))

    return render_template('blog/update.html', user=user)


def user_get(user_name):
    db = get_db()
    user = db.execute(
        'SELECT *'
        ' FROM user'
        ' WHERE username = ?',
        (user_name,)
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