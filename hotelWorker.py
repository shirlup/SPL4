import sys
import sqlite3
import os

databaseExisted = os.path.isfile('cronhoteldb.db')
if databaseExisted:
    connect = sqlite3.connect('cronhoteldb.db')
    c = connect.cursor()

# parameter is the room number.
# return the time t the tas kwas

def dohoteltask(taskname, parameter):
    if taskname == "clean":
        c.execute("""SELECT RoomNumber FROM Rooms EXCEPT SELECT RoomNumber FROM Residents""")
        rooms_to_clean = c.fetchall()  # list of all rooms that we need to clean
        time = str(sqlite3.time.time())
        print "Rooms ",
        for a_num in rooms_to_clean:  # iterates through each tuple
            sys.stdout.write( str(a_num[0]))
            if a_num != rooms_to_clean[-1]:
                print ",",
        print " were cleaned at " + time
        return float(time)
    elif taskname == "wakeup":
        resident = getResidentByRoomNum(parameter)
        time = str(sqlite3.time.time())
        print "%s %s in room %s received a wakeup call at %s" % (resident[0], resident[1], parameter, time)
        return float(time)

    #if breakfast:
    else:
        resident = getResidentByRoomNum(parameter)
        time = str(sqlite3.time.time())
        print "%s %s in room %s has been served breakfast at %s" % (resident[0], resident[1], parameter, time)
        return float(time)


def getResidentByRoomNum(parameter):
    c.execute("""SELECT FirstName,LastName FROM Residents WHERE RoomNumber IS (?)""", (parameter,))
    resident = c.fetchall()[0]
    return resident
