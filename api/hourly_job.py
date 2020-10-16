from Model import *

for user in User.getAllUser():
    print('Staring to check exam to archive for user '+ str(user) +'.')
    ui = user['userid']
    completed_exam = Exam.getCompletedExamForUser(ui)
    completed_exam.sort()
    print('List of completed exams: '+ str(completed_exam))
    l = len(completed_exam)
    if l < 2 :
        print('Nothing to archive for the user.')
    else :
        c = 0
        while c < ( l - 1 ) :
            e = completed_exam[c]
            c += 1
            print('Starting to archive: ' + str(e))
            tq = 0
            ts = 0
            ql = ExamQuestion.getExamQuestion(e)
            for q in ql :                
                tq += 1
                qd = Question.getQuestionById(q['questionid'])
                print('Considering Question: '+ str(qd))
                if q['choice'] == qd['answer'] :
                    qs = 1
                    ts += 1
                else :
                    qs = 0
                ReportQuestion.addReportQuestion(ui, qd['subject'], qd['difficulty'], qs)
            print('Report Question: '+ str(ReportQuestion.getReportQuestion(ui)))
            pp = app.config['EXAM_PASS_PERCENTAGE']
            tp = (ts / tq) * 100
            if tp > pp :
                hp = 1
            else :
                hp = 0
            ed = Exam.getExamById(e)
            print('Exam Details: '+ str(ed))
            ts = (ed['endtime'] - ed['starttime']).total_seconds()
            tm = int(ts/60)
            ReportExam.addExam(ui, hp, tm)
            print('Report Exam: '+str(ReportExam.getReportExam(ui)))
            ExamQuestion.deleteExamQuestion(e)
            Exam.deleteExam(e)
            ReportQuestion.commitSession()
            ReportExam.commitSession()
            ExamQuestion.commitSession()
            Exam.commitSession()
            
            
                




        