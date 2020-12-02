import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/description', methods=('GET', 'POST'))
def description():
    return render_template('auth/description.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        tel = request.form['tel']
        mail = request.form['mail']
        # weight = request.form['weight']
        # height = request.form['height']
        # gender = request.form['gender']
        # course = request.form['course']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # db.execute(
            #     'INSERT INTO user (username, password, address, weight, height, gender, course) '
            #     'VALUES (?, ?, ?, ?, ?, ?, ?)',
            #     (username, generate_password_hash(password), address, weight, height, gender, course)
            # )
            # db.commit()
            # return redirect(url_for('auth.login'))
            return redirect(
                url_for('auth.profile',
                    username = username,
                    password = password,
                    address = address,
                    tel = tel,
                    mail = mail
                )
            )

        flash(error)

    return render_template('auth/register.html')

@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    if request.method == 'POST':
        username = request.args.get("username")
        password = request.args.get("password")
        address = request.args.get("address")
        tel = request.args.get("tel")
        mail = request.args.get("mail")
        weight = request.form['weight']
        height = request.form['height']
        gender = request.form['gender']
        return redirect(
            url_for('auth.allergies',
                username = username,
                password = password,
                address = address,
                tel = tel,
                mail = mail,
                weight = weight,
                height = height,
                gender = gender
            )
        )
    # return redirect(url_for('auth.login'))
    return render_template('auth/profile.html')

@bp.route('/allergies', methods=('GET', 'POST'))
def allergies():
    if request.method == 'POST':
        username = request.args.get("username")
        password = request.args.get("password")
        address = request.args.get("address")
        tel = request.args.get("tel")
        mail = request.args.get("mail")
        weight = request.args.get('weight')
        height = request.args.get('height')
        gender = request.args.get('gender')
        allergies = request.form.getlist('allergies')
        # allergies_list = ["egg", "milk", "wheat", "shrimp", "crab", "peanuts", "soba"]
        # for item_outer in allergies:
        #     for item_inner in allergies_list:
        #         if item_outer == item_inner:

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
        print("username: {}".format(username))
        print("password: {}".format(password))
        print("address: {}".format(address))
        print("tel: {}".format(tel))
        print("mail: {}".format(mail))
        print("weight: {}".format(weight))
        print("height: {}".format(height))
        print("gender: {}".format(gender))
        print("allergies: {}".format(allergies))

        db = get_db()
        db.execute(
            'INSERT INTO user (username, password, address, tel, weight, height, gender, egg, milk, wheat, shrimp, crab, peanuts, soba) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (username, generate_password_hash(password), address, tel, weight, height, gender, egg, milk, wheat, shrimp, crab, peanuts, soba)
        )
        db.commit()
        return redirect(url_for('auth.login'))
        
    return render_template('auth/allergies.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_name'] = user['username']
            return redirect(url_for('blog.profile', user_name=session['user_name']))
        
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view