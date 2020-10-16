from Model import *
import smtplib, ssl

port = 465 
smtp_server = "smtp.gmail.com"
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
admin_email = User.getUserById(0)['email']
admin_password = User.getUserById(0)['password']
print('Admin Email id: '+ str(admin_email) +'.')

# Notification for Exam Count Update Request
print('Starting - Notification for Exam Count Update Request')
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(admin_email, admin_password)
    tracker_list = ExamCountTracker.getExamCountTrackerNotNotified()
    if tracker_list :
        for tracker in ExamCountTracker.getExamCountTrackerNotNotified() :
            print(tracker)
            userid = tracker['userid']
            tid = tracker['examcounttrackerid']
            print('Found request for user '+ str(userid) +'.')
            user = User.getUserById(userid)
            user_email = user['email']
            user_name = user['name']
            exam_count = tracker['examcount']
            print('Sending notification for user name '+ str(user_name) +' to user email '+ str(user_email) +'.')   
            message = '''From: {0}
To: {1}
MIME-Version: 1.0
Content-type: text/html
Subject: Approve Exam Count Update

<h3>Kindly Approve : </h3>
<br>
User Id: <b>{2}</b>,
<br>
Name: <b>{3}</b>,
<br>
Exam Count Addition Request: <b>{4}</b>

<br>
<br>
Thanks.'''.format(admin_email, [ user_email, admin_email ], tracker['userid'], user_name, exam_count)
            server.sendmail(admin_email, [ user_email, admin_email ], message)
            ExamCountTracker.updateExamCountTrackerAlreadyNotified(tid)
            ExamCountTracker.commitSession()
    else :
        print('No approval notification pending.')

# Notification for Query
print('Starting - Notification for Query')
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(admin_email, admin_password)
    queryreports = QueryReport.getAllQuery()
    if queryreports :
        for queryreport in queryreports :
            id = queryreport['queryid']
            email = queryreport['email']
            querytext = queryreport['querytext']
            print('Sending notification for query from user ' +str(email)+ '.')
            message = '''From: {0}
To: {1}
MIME-Version: 1.0
Content-type: text/html
Subject: User Query

<h3>Query : </h3>
<br>
From: <b>{2}</b>,
<br>
Text: <b>{3}</b>,
<br>
<br>

Thanks.'''.format(admin_email, [ email, admin_email ], email, querytext)
            server.sendmail(admin_email, [ email, admin_email ], message)
            QueryReport.deleteQuery(id)
            QueryReport.commitSession()
    else :
        print('No query notification pending.')

