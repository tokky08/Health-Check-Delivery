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
            return redirect(url_for('auth.register_profile', username=username))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/register_profile', methods=('GET', 'POST'))
def register_profile():
    if request.method == 'POST':
        weight = request.form['weight']
        height = request.form['height']
        gender = request.form['gender']
        return redirect(url_for('auth.register_allergies', gender=gender))
    username = request.args.get("username")
    print(username)
    # return redirect(url_for('auth.login'))
    return render_template('auth/profile.html')

@bp.route('/register_allergies', methods=('GET', 'POST'))
def register_allergies():
    if request.method == 'POST':
        egg = request.form.getlist('allergies')
        # milk = request.form['milk']
        # wheat = request.form['wheat']
        # shrimp = request.form['shrimp']
        # crab = request.form['crab']
        # peanuts = request.form['peanuts']
        # soba = request.form['soba']
        print("egg: {}".format(egg))
        # print("milk: {}".format(milk))
        # print("wheat: {}".format(wheat))
        # print("shrimp: {}".format(shrimp))
        # print("crab: {}".format(crab))
        # print("peanuts: {}".format(peanuts))
        # print("soba: {}".format(soba))
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