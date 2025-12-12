from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, g
)
from werkzeug.exceptions import abort

from rrm.student import login_required, admin_required
from rrm.db import query_all, query_one, execute


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@admin_required
def dashboard():
    # in students table there is a boolean column "is_checkedin"
    n_occupied = query_one('SELECT COUNT(*) AS count FROM students WHERE is_checkedin = TRUE')
    total = 50  # hardcoded total rooms
    return render_template('admin/dashboard.html', n_occupied=n_occupied['count'], total=total)


@bp.route('/checkin', methods=['POST'])
@admin_required
def checkin():
    regno = request.form.get("regno") or request.form.get("manual_regno")
    n_occupied = query_one('SELECT COUNT(*) AS count FROM students WHERE is_checkedin = TRUE')
    total = 50  # hardcoded total rooms
    student = query_one('SELECT * FROM students WHERE regno = %s', (regno,))
    if student is None:
        flash(f'Student with registration number {regno} does not exist.', 'error')
    elif student['is_checkedin']:
        execute('UPDATE students SET is_checkedin = FALSE WHERE regno = %s', (regno,))
        execute("UPDATE entries SET out_time = NOW() AT TIME ZONE 'Asia/Kolkata' WHERE regno = %s AND out_time IS NULL",
                (student['regno'],))
        flash(f'Student {student["name"]} checked out successfully.', 'success')
    elif n_occupied['count'] >= total:
        flash('No rooms available for check-in.', 'error')
    else:
        execute('UPDATE students SET is_checkedin = TRUE WHERE regno = %s', (regno,))
        execute("INSERT INTO entries (regno, name, branch, in_time) VALUES (%s, %s, %s, NOW() AT TIME ZONE 'Asia/Kolkata')",
                (student['regno'], student['name'], student['branch']))
        flash(f'Student {student["name"]} checked in successfully.', 'success')
    return redirect(url_for('admin.dashboard'))


@bp.route('/entries/<int:page>')
@admin_required
def entries(page):
    # pagination will be according to in_time dates one page has all entries of a particular date and date also in format DD-MM-YYYY
    dates = query_all("SELECT DISTINCT DATE(in_time AT TIME ZONE 'Asia/Kolkata') AS in_time FROM entries ORDER BY in_time DESC")
    if page < 1 or page > len(dates):
        flash('Invalid page number.', 'error')
        return redirect(url_for('admin.entries', page=1))
    entry_date = dates[page - 1]['in_time']

    entries = query_all("SELECT session_id, regno, name, branch, to_char(in_time, 'HH12:MI AM') AS in_time_formatted, to_char(out_time, 'HH12:MI AM') AS out_time_formatted FROM entries WHERE DATE(in_time AT TIME ZONE 'Asia/Kolkata') = %s ORDER BY in_time DESC", (entry_date,))
    return render_template('admin/allentries.html', entries=entries, entry_date=entry_date, page=page, total_pages=len(dates))
    # return the timestamps in the format of only date and time without timezone info that too in Am-PM format
    # entries = query_all("SELECT session_id, regno, name, branch, to_char(in_time, 'HH12:MI AM DD-MM-YYYY') AS in_time_formatted, to_char(out_time, 'HH12:MI AM DD-MM-YYYY') AS out_time_formatted FROM entries ORDER BY in_time DESC")
    # return render_template('admin/allentries.html', entries=entries)