import smtplib
from .db import query_all, execute

def sendReminder(query_all, execute, app):
    # bring the students with set_reminder = TRUE and reminder_time within the last 20 minutes
    emails = query_all("SELECT email FROM students WHERE reminder_time!=NULL AND reminder_time >= NOW() AT TIME ZONE 'Asia/Kolkata' - INTERVAL '20 minutes'")
    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = app.config['SEMAIL']
    sender_password = app.config['SPASSWORD']
    # Create the email message
    subject = 'Reminder: Box Available'
    body = 'A box has become available in the reading room.'
    message = f'Subject: {subject}\n\n{body}'
    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, emails, message)
        server.quit()
    except Exception as e:
        pass
    execute('UPDATE students SET reminder_time=NULL WHERE reminder_time!=NULL')