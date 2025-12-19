from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, g
)
from werkzeug.exceptions import abort
from datetime import datetime, timedelta

from rrm.student import login_required, admin_required
from rrm.db import query_all, query_one, execute


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@admin_required
def dashboard():
    laptop_occupied = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = TRUE AND regno IS NOT NULL')['count']
    non_laptop_occupied = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = FALSE AND regno IS NOT NULL')['count']
    total_laptop = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = TRUE')['count']
    total_non_laptop = query_one('SELECT COUNT(*) AS count FROM boxes WHERE is_laptop = FALSE')['count']
    boxes = query_all('SELECT box_no, is_laptop, regno, name, (12 * (y_coordinate - 1) + x_coordinate) AS cell_value FROM boxes ORDER BY cell_value ASC')
    cell_values = [box['cell_value'] for box in boxes]
    return render_template('admin/dashboard.html', current_date=datetime.now().date(), laptop_occupied=laptop_occupied, non_laptop_occupied=non_laptop_occupied, total_laptop=total_laptop, total_non_laptop=total_non_laptop, boxes=boxes, cell_values=cell_values)



@bp.route('/checkin', methods=['POST'])
@admin_required
def checkin():
    regno = request.form.get("regno") or request.form.get("manual_regno")
    preferred_box = request.form.get("preferred_box")
    n_occupied = query_one('SELECT COUNT(*) AS count FROM students WHERE is_checkedin = TRUE')
    total = query_one('SELECT COUNT(*) AS count FROM boxes')['count']
    student = query_one('SELECT * FROM students WHERE regno = %s', (regno,))

    if student is None:
        flash(f'Student with registration number {regno} does not exist.', 'danger')
    
    elif student['is_checkedin']:
        execute('UPDATE students SET is_checkedin=FALSE, box_no=NULL WHERE regno = %s', (regno,))
        execute('UPDATE boxes SET regno=NULL, name=NULL WHERE regno = %s', (regno,))
        execute("UPDATE entries SET out_time = NOW() AT TIME ZONE 'Asia/Kolkata' WHERE regno = %s AND out_time IS NULL",
                (student['regno'],))
        flash(f'Student {student["name"]} checked out successfully.', 'success')
    
    elif n_occupied['count'] >= total:
        flash('No rooms available for check-in.', 'danger')
    
    else:
        if student['preferred_box']:
            box = query_one('SELECT box_no FROM boxes WHERE box_no = %s AND regno IS NULL', (student['preferred_box'],))
            if box is None:
                flash(f'Preferred box {student["preferred_box"]} is not available. Assigning a different box.', 'warning')
            else:
                execute('UPDATE students SET is_checkedin = TRUE, box_no = %s, preferred_box = NULL WHERE regno = %s', (box['box_no'], regno))
                execute('UPDATE boxes SET regno = %s, name = %s WHERE box_no = %s', (regno, student['name'], box['box_no']))
                execute("INSERT INTO entries (regno, name, branch, box_no, in_time) VALUES (%s, %s, %s, %s, NOW() AT TIME ZONE 'Asia/Kolkata')",
                        (student['regno'], student['name'], student['branch'], box['box_no']))
                flash(f'Student {student["name"]} checked into preferred box {box["box_no"]} successfully.', 'success')
                return redirect(url_for('admin.dashboard'))
        elif preferred_box:
            box = query_one('SELECT box_no FROM boxes WHERE box_no = %s AND regno IS NULL', (preferred_box,))
            if box is None:
                flash(f'Selected box {preferred_box} is not available. Assigning a different box.', 'warning')
            else:
                execute('UPDATE students SET is_checkedin = TRUE, box_no = %s WHERE regno = %s', (box['box_no'], regno))
                execute('UPDATE boxes SET regno = %s, name = %s WHERE box_no = %s', (regno, student['name'], box['box_no']))
                execute("INSERT INTO entries (regno, name, branch, box_no, in_time) VALUES (%s, %s, %s, %s, NOW() AT TIME ZONE 'Asia/Kolkata')",
                        (student['regno'], student['name'], student['branch'], box['box_no']))
                flash(f'Student {student["name"]} checked into box {box["box_no"]} successfully.', 'success')
                return redirect(url_for('admin.dashboard'))
        elif student['is_laptop']:
            box = query_one('SELECT box_no FROM boxes WHERE is_laptop=TRUE AND regno IS NULL ORDER BY box_no ASC')
            if box is None:
                box = query_one('SELECT box_no FROM boxes WHERE regno IS NULL')
        else:
            box = query_one('SELECT box_no FROM boxes WHERE is_laptop=FALSE AND regno IS NULL ORDER BY box_no ASC')
            if box is None:
                box = query_one('SELECT box_no FROM boxes WHERE regno IS NULL')
        
        execute('UPDATE students SET is_checkedin = TRUE, box_no = %s WHERE regno = %s', (box['box_no'], regno))
        execute('UPDATE boxes SET regno = %s, name = %s WHERE box_no = %s', (regno, student['name'], box['box_no']))
        execute("INSERT INTO entries (regno, name, branch, box_no, in_time) VALUES (%s, %s, %s, %s, NOW() AT TIME ZONE 'Asia/Kolkata')",
                (student['regno'], student['name'], student['branch'], box['box_no']))
        flash(f'Student {student["name"]} checked into box {box["box_no"]} successfully.', 'success')
    
    return redirect(url_for('admin.dashboard'))


@bp.route('/entries/<string:date>', methods=['GET', 'POST'])
@admin_required
def entries(date):
    if request.method == 'POST':
        entry_date = request.form.get('entry_date')
        return redirect(url_for('admin.entries', date=entry_date))
    # date will be a string in yyyy-mm-dd format
    entry_date = datetime.strptime(date, '%Y-%m-%d').date()
    previous_date = entry_date - timedelta(days=1)
    next_date = entry_date + timedelta(days=1)
    entries = query_all("SELECT session_id, regno, box_no, name, branch, to_char(in_time, 'HH12:MI AM') AS in_time_formatted, to_char(out_time, 'HH12:MI AM') AS out_time_formatted FROM entries WHERE in_time::date = %s ORDER BY in_time DESC", (entry_date,))
    return render_template('admin/entries.html', current_date=datetime.now().date(), entries=entries, entry_date=entry_date, previous_date=previous_date, next_date=next_date)


@bp.route('/box-control')
@admin_required
def box_control():
    boxes = query_all('SELECT box_no, is_laptop, regno, name, (12 * (y_coordinate - 1) + x_coordinate) AS cell_value FROM boxes ORDER BY cell_value ASC')
    cell_values = [box['cell_value'] for box in boxes]
    return render_template('admin/boxcontrol.html', boxes=boxes, cell_values=cell_values)