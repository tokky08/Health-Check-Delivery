from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import time
import datetime

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    return render_template('blog/top.html')


@bp.route('/<user_name>/cancel', methods=('GET', 'POST'))
def cancel(user_name):
    created = request.args.get("created")
    db = get_db()
    db.execute('DELETE FROM ordered WHERE created = ?', (created,))
    db.commit()

    return redirect(url_for('blog.profile', user_name=user_name))

@bp.route('/<user_name>/cancel_1', methods=('GET', 'POST'))
def cancel_1(user_name):
    created= request.args.get("created")
    db = get_db()
    db.execute('DELETE FROM ordered WHERE created = ?', (created,))

    menu_id = request.args.get("menu_id")
    eat_time = request.args.get("eat_time")
    menu = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE id = ?',
        (menu_id,)
    ).fetchone()
    db.commit()

    # return redirect(url_for('blog.detail', user_name=user_name))
    # return render_template('blog/detail.html', user_name=user_name, menu_id=menu_id, menu=menu, eat_time=eat_time, ordered_created=ordered["created"], dt_now=dt_now)
    return render_template('blog/detail.html', user_name=user_name, menu=menu, eat_time=eat_time)

@bp.route('/<user_name>/ordered', methods=('GET', 'POST'))
def ordered(user_name):
    menu_id = request.args.get("menu_id")
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
    delivery_time = request.args.get("delivery_time")
    
    db.execute(
        'INSERT INTO ordered (menuid, username, menuname, img, eattime, type, calorie, deliverytime, details)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (menu_id, user_name, menuname, img, eattime, type_bmi, calorie, delivery_time, details)
    )
    db.commit()

    return redirect(url_for('blog.profile', user_name=user_name))


@bp.route('/<user_name>/profile', methods=('GET', 'POST'))
def profile(user_name):
    user = user_get(user_name)
    bmi = bmi_get(user)
    menu_id = request.args.get("menu_id")
    
    db = get_db()
    user = db.execute(
        'SELECT *'
        ' FROM user'
        ' WHERE username = ?',
        (user_name,)
    ).fetchone()

    if user["gender"] == "male":
        img_gender = "male"
    else:
        img_gender = "female"

    if bmi < 20:
        img_type = "slim"
        bmi_type = "低体重タイプ"
        disc_type = "あなたは痩せ気味のため、毎日３食しっかり摂取し、適正体重の維持とバランスのとれた食生活の確立を目指しましょう。"
    elif 25 < bmi:
        img_type = "plump"
        bmi_type = "肥満タイプ"
        disc_type = "あなたは肥満気味のため、野菜やキノコ類、海藻類など栄養豊富なものを摂取し、規則正しい食事を送ることを心がけましょう。"
    else:
        img_type = "standard"
        bmi_type = "標準タイプ"
        disc_type = "あなたは健康的な体です。このままの状態を維持し、毎日健康的な食生活を送りましょう。"
        
    return render_template('blog/profile.html',
        user_name=user_name,
        bmi=bmi,
        bmi_type = bmi_type,
        disc_type = disc_type,
        img_gender=img_gender,
        img_type = img_type
    )

@bp.route('/<user_name>/check', methods=('GET', 'POST'))
def check(user_name):
    delivery_time = request.form["delivery_time"]
    menu_id = request.args.get("menu_id")
    db = get_db()
    menu = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE id = ?',
        (menu_id,)
    ).fetchone()

    eat_time = request.args.get("eat_time")
    ordered = db.execute(
        'SELECT *'
        ' FROM ordered'
        ' WHERE eattime = ? and username = ?'
        ' ORDER BY created DESC',
        (eat_time, user_name,)
    ).fetchone()

    if ordered:
        print(ordered["created"].strftime('%Y-%m-%d'))
        ordered_time = db.execute(
            'SELECT datetime(?, "localtime")',
            (ordered["created"],)
        ).fetchone()
        
        ordered_time = ordered_time[0].split(" ")
        ordered_time = ordered_time[0]
        dt_now = str(datetime.datetime.now())
        dt_now = dt_now.split(" ")
        dt_now = dt_now[0]

        # 最終注文日が現在日と同じならばポップアップ形式でキャンセルするかを聞くような形にする
        if ordered_time == dt_now:
            return render_template('blog/detail.html', user_name=user_name, menu_id=menu_id, menu=menu, eat_time=eat_time, ordered_created=ordered["created"], dt_now=dt_now)

    return render_template('blog/check.html',
        user_name=user_name,
        menu_id=menu_id,
        menu=menu,
        delivery_time=delivery_time
    )
    

@bp.route('/<user_name>/menu/<int:bmi>', methods=('GET', 'POST'))
def menu(user_name, bmi):
    type_bmi = "low" if bmi < 20 else "high"
    eat_time = request.args.get("eat_time")

    db = get_db()
    menus = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE eattime = ? and type = ?'
        ' LIMIT 3',
        (eat_time, type_bmi,)
    ).fetchall()

    return render_template('blog/order.html', eat_time=eat_time, menus=menus, user_name=user_name)

@bp.route('/<user_name>/detail', methods=('GET', 'POST'))
def detail(user_name):
    menu_id = request.args.get("menu_id")
    eat_time = request.args.get("eat_time")
    db = get_db()
    menu = db.execute(
        'SELECT *'
        ' FROM menu'
        ' WHERE id = ?',
        (menu_id,)
    ).fetchone()
    return render_template('blog/detail.html', user_name=user_name, menu_id=menu_id, menu=menu, eat_time=eat_time)


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

    nowtime_list = []
    for time in logs:
        ordered_time = db.execute(
            'SELECT datetime(?, "localtime")',
            (time["created"],)
        ).fetchone()
        nowtime_list.append(ordered_time[0])

    return render_template('blog/log.html', logs=logs, nowtime_list=nowtime_list, user_name=user_name)

@bp.route('/<user_name>/status', methods=('GET', 'POST'))
def status(user_name):
    user = user_get(user_name)
    bmi = bmi_get(user)
    db = get_db()
    status = db.execute(
        'SELECT *'
        ' FROM ordered o JOIN user u ON o.username = u.username'
        ' WHERE o.username = ?'
        ' ORDER BY created DESC',
        (user_name,)
    ).fetchall()

    nowtime_list = []
    for time in status:
        ordered_time = db.execute(
            'SELECT datetime(?, "localtime")',
            (time["created"],)
        ).fetchone()
        nowtime_list.append(ordered_time[0])

    dt_now = datetime.datetime.now()
    dt_now = str(dt_now).split("-")
    dt_now_2 = dt_now[2].split(" ")
    dt_now_list = []
    dt_now_list.append(dt_now[0])
    dt_now_list.append(dt_now[1])
    dt_now_list.append(dt_now_2[0])
    dt_now_list.append(dt_now_2[1])
    dt_now_time = dt_now_list[3].split(":")
    year = int(dt_now_list[0])
    month= int(dt_now_list[1])
    day = int(dt_now_list[2])
    hour = int(dt_now_time[0])
    minutes = int(dt_now_time[1])
    time_check_list = []

    year_f = None
    month_f =  None
    day_f =  None

    for i in status:
        feature_date = i["created"] + datetime.timedelta(days=1)
        feature_date = db.execute(
            'SELECT datetime(?, "localtime")',
            (feature_date,)
        ).fetchone()
        feature_date = feature_date[0].split("-")
        feature_date_2 = feature_date[2].split(" ")
        feature_date_list = []
        feature_date_list.append(feature_date[0])
        feature_date_list.append(feature_date[1])
        feature_date_list.append(feature_date_2[0])
        feature_date_list.append(i["deliverytime"])
        feature_time = feature_date_list[3].split(":")
        year_f = int(feature_date_list[0])
        month_f = int(feature_date_list[1])
        day_f = int(feature_date_list[2])
        hour_f = int(feature_time[0])
        minutes_f = int(feature_time[1])
        now = datetime.datetime(year,month,day,hour,minutes,0)
        feature = datetime.datetime(year_f,month_f,day_f,hour_f,minutes_f,0)

        time_check_list.append(now < feature)
    
    return render_template('blog/status.html',
        status=status,
        user_name=user_name,
        bmi=bmi,
        nowtime_list=nowtime_list,
        time_check_list=time_check_list,
        year_f=year_f,
        month_f=month_f,
        day_f=day_f
    )

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

    return render_template('blog/update.html', user=user, user_name=user_name)


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