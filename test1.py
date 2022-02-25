import mysql.connector
mydb = mysql.connector.connect(host='localhost',user='admin',password='#admin',database='dbs')
cursor = mydb.cursor()
cursor.execute("SELECT Name FROM classxii")

for x in mydb.cursor():
    print(x)
