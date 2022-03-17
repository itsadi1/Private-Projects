import datetime,webbrowser,sys
from mysql.connector import connect

def admin():
    password = '#admin'
    mydb = connect(
            host='localhost',
            user='admin',
            password=password,
            database = 'dbs')
    return(mydb,password)

def guest():
    password = '#guest'
    mydb = connect(
            host = 'localhost',
            user = 'guest',
            password = password,
            database = 'dbs')
    return(mydb,password)

def PassWord(attempts):
    if attempts != 0:
        Password = input('Enter password:')

        if Password == password:
            print('User Verified!')
            print('Welcome {}'.format(username))

        else:

            if attempts-1 !=0:
                print('Incorrect Password! Remaining Attempts:{}'.format(attempts-1))

            else:
                print('User Not Verified!')

            PassWord(attempts-1)

    else:
        sys.exit()

username = input('Enter User:')

def Nm(mydb):
    Mstuname = input('Enter Student Name:')
    Mstuno = int(input('Enter Student Id.'))
    MDate = input('Enter Date (YYYY-MM-DD):')
    MTime = input('Enter Time (hh:mm:ss):')
    MLink = input('Enter Meeting Link:')
    mydb.cursor().execute('''INSERT INTO classxii(
        Name,Id,Date,Time,Link,Attendance) 
        VALUES(%s,%s,%s,%s,%s,%s)''',
    (Mstuname,Mstuno,MDate,MTime,MLink,'A'))
    mydb.commit()

def Ca(cursor):
    cursor.execute('SELECT Name,Id FROM classxii WHERE Attendance = "P"')
    results = cursor.fetchall()

    for i in results:
        print(i)

def Cm(mydb,cursor):
    iD = int(input('Enter Student Id:'))
    dATE = (str(datetime.datetime.now()).split(' ')[0]).split('-')
    tIME = str(str(str(datetime.datetime.now()).split(' ')[-1]).split('.')[0]).split(':')
    YYYY,MM,DD = dATE
    HH,M,_ = tIME
    cursor.execute('SELECT Sno,Name,Time,Link FROM classxii WHERE Id = %s AND Date = %s',
    (iD, datetime.date(int(YYYY),int(MM),int(DD))))
    results = cursor.fetchall()

    for i in results:
        print('Student Found:{}'.format(i[1]))
        tiME = i[2]
        hh,mm,_ = str(tiME).split(':')

        if hh>=HH:

            if mm>=M:
                print('Meeting Scheduled')

            else:
                print('You are running Late..')

            print('Meeting Link:{}'.format(i[-1]))
            om = input('Join Meeting(y/n):')

            if om == 'y':webbrowser.open(i[-1])

            cursor.execute('UPDATE classxii SET Attendance = "P" WHERE Sno = %s',(i[0],))
            mydb.commit()

if username.lower() == 'admin':
    mydb,password = admin()
    PassWord(3)
    mydb.cursor().execute('CREATE DATABASE IF NOT EXISTS classxii ')
    mydb.cursor().execute('''CREATE TABLE IF NOT EXISTS classxii(
    Sno INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(20),
    Id INT,
    Date DATE,
    Time TIME,
    Link VARCHAR(100),
    Attendance VARCHAR(1))''')

    while True:
        nm = input("New Meeting (y/n):")

        if nm == 'y': Nm(mydb)
        ca = input('Check Attendance (y/n):')

        if ca == 'y': Ca(mydb.cursor())
        exit = input("Exit (y/n):")

        if exit == 'y': sys.exit()

elif username.lower() == 'guest':
    mydb,password = guest()
    PassWord(3)
    Cm(mydb,mydb.cursor())
    exit = input('Exit (y/n):')

    if exit == 'y': sys.exit()

else:
    print('User not Found!')
    sys.exit()
