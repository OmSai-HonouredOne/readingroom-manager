import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from rrm.db import query_all, query_one, execute


bp = Blueprint('student', __name__)


@bp.before_app_request
def load_logged_in_user():
    regno = session.get('user_regno')

    if regno is None:
        g.user = None
    else:
        g.user = query_one('SELECT * FROM students WHERE regno = %s', (regno,))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('student.login'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user['is_admin']:
            return redirect(url_for('student.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/')
def home():
    n_occupied = query_one('SELECT COUNT(*) AS count FROM students WHERE is_checkedin = TRUE')
    total = 50  # hardcoded total rooms
    return render_template('student/home.html', student=g.user, n_occupied=n_occupied['count'], total=total)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if g.user is not None:
        return redirect(url_for('student.profile'))
    else:
        if request.method == 'POST':
            regno = request.form['regno']
            name = request.form['name']
            branch = request.form['branch']
            email = request.form['email']
            password = request.form['password']
            cpassword = request.form['cpassword']
            error = None

            if not regno:
                error = 'Registration number is required.'
            elif not password:
                error = 'Password is required.'
            elif query_one('SELECT regno FROM students WHERE regno = %s', (regno,)) is not None:
                error = f'User {regno} is already registered.'
            elif password != cpassword:
                error = 'Passwords do not match.'

            if error is None:
                execute(
                    'INSERT INTO students (regno, name, branch, email, password) VALUES (%s, %s, %s, %s, %s)',
                    (regno, name, branch, email, generate_password_hash(password))
                )
                return redirect(url_for('student.login'))

            flash(error, 'danger')

        return render_template('student/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('student.profile'))
    else:
        if request.method == 'POST':
            regno = request.form['regno']
            password = request.form['password']
            error = None
            user = query_one('SELECT regno, password, is_admin FROM students WHERE regno = %s', (regno,))
            print(user)

            if user is None:
                error = 'Incorrect registration number.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_regno'] = user['regno']
                if user['is_admin']:
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('student.profile'))
            
            flash(error, 'danger')

    return render_template('student/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('student.home'))


@bp.route('/profile')
@login_required
def profile():
    n_occupied = query_one('SELECT COUNT(*) AS count FROM students WHERE is_checkedin = TRUE')
    total = 50  # hardcoded total rooms
    return render_template('student/profile.html', student=g.user, n_occupied=n_occupied['count'], total=total)

@bp.route('/edit/<int:regno>', methods=('GET', 'POST'))
@login_required
def editprofile(regno):
    if g.user['regno'] != regno:
        flash("You are not authorized to edit this profile.", 'danger')
        print(g.user['regno'], regno)
        return redirect(url_for('student.profile'))

    if request.method == 'POST':
        name = request.form['name']
        branch = request.form['branch']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']
        error = None

        if not name:
            error = 'Name is required.'
        elif not branch:
            error = 'Branch is required.'
        elif not email:
            error = 'Email is required.'
        elif password and password != cpassword:
            error = 'Passwords do not match.'
        if error is None:
            if password:
                execute(
                    'UPDATE students SET name = %s, branch = %s, email = %s, password = %s WHERE regno = %s',
                    (name, branch, email, generate_password_hash(password), regno)
                )
            else:
                execute(
                    'UPDATE students SET name = %s, branch = %s, email = %s WHERE regno = %s',
                    (name, branch, email, regno)
                )
            return redirect(url_for('student.profile'))

        flash(error, 'danger')

    return render_template('student/editprofile.html', student=g.user)