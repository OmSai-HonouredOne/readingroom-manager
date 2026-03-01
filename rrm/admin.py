from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, g, current_app
)
from werkzeug.exceptions import abort
from datetime import datetime, timedelta

from rrm.student import login_required, admin_required
from rrm.db import query_all, query_one, execute
from .layout import layoutnp
from .reminder import sendReminder


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html', layoutnp=layoutnp, current_date=datetime.now().date())



@bp.route('/checkin', methods=['POST'])
@admin_required
def checkin():
    regno = request.form.get("regno") or request.form.get("manual_regno")
    preferred_box = request.form.get("preferred_box")
    
    # if None type then no conversion
    if preferred_box:
        preferred_box=int(preferred_box)
    if regno:
        regno=int(regno)


    # n_occupied = query_one('SELECT COUNT(*) AS count FROM students WHERE is_checkedin = TRUE')
    n_occupied = layoutnp[layoutnp['regno']>1].size
    # total = query_one('SELECT COUNT(*) AS count FROM boxes')['count']
    total = layoutnp[layoutnp['regno']>0].size
    student = query_one('SELECT * FROM students WHERE regno = %s', (regno,))

    # if account doesnt exist or invalid registration number
    if student is None:
        flash(f'Student with registration number {regno} does not exist.', 'danger')
    
    # in checked in, then check out
    elif student['box_no']:
        # execute('UPDATE boxes SET regno=NULL, name=NULL WHERE regno = %s', (regno,))
        layoutnp['regno'][layoutnp['regno']==regno] = 1
        execute('UPDATE students SET box_no=NULL WHERE regno = %s', (regno,))
        execute("UPDATE entries SET out_time = NOW() AT TIME ZONE 'Asia/Kolkata' WHERE regno = %s AND out_time IS NULL",
                (student['regno'],))
        
        flash(f'Student {student["name"]} checked out successfully.', 'success')
        sendReminder(query_all, execute, current_app)
    elif n_occupied >= total:
        flash('No rooms available for check-in.', 'danger')
    
    else:
        # If student has a preference of seats
        if student['preferred_box']:
            # box = query_one('SELECT box_no FROM boxes WHERE box_no = %s AND regno IS NULL', (student['preferred_box'],))
            box = layoutnp['box_no'][(layoutnp['regno']==1) & (layoutnp['box_no']==student['preferred_box'])]
            if box.size==0:
                flash(f'Preferred box {student["preferred_box"]} is not available. Assigning a different box.', 'warning')
            else:
                # execute('UPDATE boxes SET regno = %s, name = %s WHERE box_no = %s', (regno, student['name'], box['box_no']))
                layoutnp['regno'][layoutnp['box_no']==box] = regno
                execute('UPDATE students SET box_no = %s, preferred_box = NULL WHERE regno = %s', (int(box[0]), regno))
                execute("INSERT INTO entries (regno, name, branch, box_no, in_time) VALUES (%s, %s, %s, %s, NOW() AT TIME ZONE 'Asia/Kolkata')",
                        (student['regno'], student['name'], student['branch'], int(box[0])))
                flash(f'Student {student["name"]} checked into preferred box {box[0]} successfully.', 'success')
                return redirect(url_for('admin.dashboard'))
        
        # If checked in through admin
        elif preferred_box:
            # box = query_one('SELECT box_no FROM boxes WHERE box_no = %s AND regno IS NULL', (preferred_box,))
            box = layoutnp['box_no'][(layoutnp['box_no']==preferred_box) & (layoutnp['regno']==1)]
            print(box, preferred_box, layoutnp['box_no'][(layoutnp['box_no']==7) & (layoutnp['regno']==1)], type(preferred_box), sep='\n')
            if box.size==0:
                flash(f'Selected box {preferred_box} is not available. Assigning a different box.', 'warning')
            else:
                # execute('UPDATE boxes SET regno = %s, name = %s WHERE box_no = %s', (regno, student['name'], box['box_no']))
                layoutnp['regno'][layoutnp['box_no']==box] = regno
                print(layoutnp['regno'])
                execute('UPDATE students SET box_no = %s WHERE regno = %s', (int(box[0]), regno))
                execute("INSERT INTO entries (regno, name, branch, box_no, in_time) VALUES (%s, %s, %s, %s, NOW() AT TIME ZONE 'Asia/Kolkata')",
                        (student['regno'], student['name'], student['branch'], int(box[0])))
                flash(f'Student {student["name"]} checked into box {box[0]} successfully.', 'success')
                return redirect(url_for('admin.dashboard'))
            
        # if student has is_laptop toggled on
        elif student['is_laptop']:
            # box = query_one('SELECT box_no FROM boxes WHERE is_laptop=TRUE AND regno IS NULL ORDER BY box_no ASC')
            box = layoutnp['box_no'][(layoutnp['is_laptop']==True) & (layoutnp['regno']==1)]
            if box.size==0:
                # box = query_one('SELECT box_no FROM boxes WHERE regno IS NULL')
                box = layoutnp['box_no'][layoutnp['regno']==1]
        
        # if student has is_laptop toggled off
        else:
            # box = query_one('SELECT box_no FROM boxes WHERE is_laptop=FALSE AND regno IS NULL ORDER BY box_no ASC')
            box = layoutnp['box_no'][(layoutnp['is_laptop']==False) & (layoutnp['regno']==1)]
            if box.size==0:
                # box = query_one('SELECT box_no FROM boxes WHERE regno IS NULL')
                box = layoutnp['box_no'][layoutnp['regno']==1]
        
        # execute('UPDATE boxes SET regno = %s, name = %s WHERE box_no = %s', (regno, student['name'], box['box_no']))
        layoutnp['regno'][layoutnp['box_no']==box[0]] = regno
        execute('UPDATE students SET box_no = %s WHERE regno = %s', (int(box[0]), regno))
        execute("INSERT INTO entries (regno, name, branch, box_no, in_time) VALUES (%s, %s, %s, %s, NOW() AT TIME ZONE 'Asia/Kolkata')",
                (student['regno'], student['name'], student['branch'], int(box[0])))
        flash(f'Student {student["name"]} checked into box {box[0]} successfully.', 'success')
    
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