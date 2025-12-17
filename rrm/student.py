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
    laptop_occupied = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = TRUE AND regno IS NOT NULL')['count']
    non_laptop_occupied = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = FALSE AND regno IS NOT NULL')['count']
    total_laptop = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = TRUE')['count']
    total_non_laptop = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = FALSE')['count']
    # another value name cell_value which equals 12*(y_coordinate-1)+x_coordinate
    boxes = query_all('SELECT box_no, is_laptop, regno, (12 * (y_coordinate - 1) + x_coordinate) AS cell_value FROM boxes ORDER BY cell_value ASC')
    cell_values = [box['cell_value'] for box in boxes]
    return render_template('student/home.html', student=g.user, boxes=boxes, cell_values=cell_values, laptop_occupied=laptop_occupied, non_laptop_occupied=non_laptop_occupied, total_laptop=total_laptop, total_non_laptop=total_non_laptop)


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
    laptop_occupied = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = TRUE AND regno IS NOT NULL')['count']
    non_laptop_occupied = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = FALSE AND regno IS NOT NULL')['count']
    total_laptop = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = TRUE')['count']
    total_non_laptop = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = FALSE')['count']
    return render_template('student/profile.html', student=g.user, laptop_occupied=laptop_occupied, non_laptop_occupied=non_laptop_occupied, total_laptop=total_laptop, total_non_laptop=total_non_laptop)


@bp.route('/profile/<int:regno>/toggle_laptop')
@login_required
def toggle_laptop(regno):
    if g.user['regno'] != regno:
        flash("You are not authorized to edit this profile.", 'danger')
        return redirect(url_for('student.profile'))

    current_status = g.user['is_laptop']
    new_status = not current_status

    execute(
        'UPDATE students SET is_laptop = %s WHERE regno = %s',
        (new_status, regno)
    )

    flash("Laptop status updated successfully.", 'success')
    return redirect(url_for('student.profile'))


@bp.route('/set_preference/<int:box_no>/<int:regno>', methods=('POST',))
@login_required
def set_preference(box_no, regno):
    if g.user['regno'] != regno:
        flash("You are not authorized to set preference for this profile.", 'danger')
        return redirect(url_for('student.home'))

    box = query_one('SELECT * FROM boxes WHERE box_no = %s', (box_no,))
    if box is None:
        flash("Invalid box number.", 'danger')
        return redirect(url_for('student.home'))

    if box['regno'] is not None:
        flash("This box is already assigned to another student.", 'danger')
        return redirect(url_for('student.home'))

    execute(
        'UPDATE students SET preferred_box = %s WHERE regno = %s',
        (box_no, regno)
    )

    flash("Box preference set successfully.", 'success')
    return redirect(url_for('student.profile'))


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