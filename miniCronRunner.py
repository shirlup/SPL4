import sqlite3
import os
import hotelWorker

databaseExisted = os.path.isfile('cronhoteldb.db')

to_terminate = False
first_time = True
if databaseExisted:
    dbcon = sqlite3.connect('cronhoteldb.db')
    cursor = dbcon.cursor()
    cursor.execute("SELECT * FROM Tasks")
    tasks = cursor.fetchall()
    time = {}
while databaseExisted and not(to_terminate):
    allTasksZero = True
    if first_time :
        for one_task in tasks :
            time[one_task[0]]= hotelWorker.dohoteltask(one_task[1],one_task[2])
            cursor.execute("UPDATE TaskTimes SET NumTimes = NumTimes-1 WHERE TaskId=(?)", (one_task[0],))
        first_time= False
    else :
        for one_task in tasks:
            cursor.execute("SELECT DoEvery FROM TaskTimes WHERE TaskId = (?)", (one_task[0],))
            do_every = cursor.fetchone()[0]
            cursor.execute("SELECT NumTimes FROM TaskTimes Where TaskId = (?)",(one_task[0],))
            num_times = cursor.fetchone()[0]
            allTasksZero = allTasksZero and num_times ==0
            if (num_times>0 and sqlite3.time.time() - time[one_task[0]] ) >= do_every:
                time[one_task[0]]=hotelWorker.dohoteltask(one_task[1],one_task[2]) #update the list of times
                cursor.execute("UPDATE TaskTimes SET NumTimes = NumTimes-1 WHERE TaskId=(?)", (one_task[0],)) #update numtimes

        if allTasksZero :
            to_terminate = True
