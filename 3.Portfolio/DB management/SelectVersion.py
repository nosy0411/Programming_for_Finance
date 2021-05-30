import pymysql

connection = pymysql.connect(host='localhost', port=3307, db='finance', 
    user='root', passwd='1q2w3e4r', autocommit=True)  

cursor = connection.cursor()
cursor.execute("SELECT VERSION();")
result = cursor.fetchone()

print ("MariaDB version : {}".format(result))

connection.close()