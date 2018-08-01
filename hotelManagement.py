import sqlite3
import os
import sys

databaseexisted = os.path.isfile('cronhoteldb.db')
dbcon = sqlite3.connect('cronhoteldb.db')
with dbcon:
    cursor = dbcon.cursor()


def createTables():  # First time creating the database. Create the tables
    cursor.executescript("""
                              CREATE TABLE TaskTimes(
                                  TaskId INT PRIMARY KEY NOT NULL,
                                  DoEvery INT NOT NULL,
                                  NumTimes INT NOT NULL
                              );

                              CREATE TABLE Tasks(
                                  TaskId INT NOT NULL,
                                  TaskName TEXT NOT NULL,
                                  Parameter INT,

                                  FOREIGN KEY (TaskId) REFERENCES TaskTimes(TaskId),

                                  PRIMARY KEY (TaskId)
                              );

                              CREATE TABLE Rooms(
                                  RoomNumber INT PRIMARY KEY NOT NULL
                              );

                              CREATE TABLE Residents(
                                  RoomNumber INT NOT NULL,
                                  FirstName TEXT NOT NULL,
                                  LastName TEXT NOT NULL,

                                  FOREIGN KEY (RoomNumber) REFERENCES Rooms(RoomNumber),

                                  PRIMARY KEY (RoomNumber)
                              );
                          """)


if not databaseexisted:
    createTables()
    taskIdCount = 0
    for line in open(sys.argv[1]):
        line = line.rstrip('\n') #remove \n
        a_row = line.split(',')
        if (a_row[0] == "room"):
            cursor.execute("INSERT INTO Rooms VALUES(?)",(a_row[1],))
            if len(a_row) > 2:
                cursor.execute("INSERT INTO Residents VALUES(?,?,?)",(a_row[1],a_row[2], a_row[3],))

        elif (a_row[0] == "clean"):
            cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (taskIdCount,a_row[0],int(0),))
            cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (taskIdCount, a_row[1], a_row[2],))
            taskIdCount += 1

        elif (a_row[0] == "breakfast" or "wakeup"):
            cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (taskIdCount,a_row[0], a_row[2],))
            cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (taskIdCount, a_row[1], a_row[3],))
            taskIdCount += 1

dbcon.commit()
