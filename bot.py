import mysql.connector

connection = mysql.connector.connect(
    host = "192.168.1.3",
    port = "3306",
    user = "donuser",
    password = "ewq#@!",
    database = "donbon"
)
cursor = connection.cursor()
for i in range(1000):
    x = i*2
    x = [i,x]
    q = '''
    INSERT INTO test (test, test2) 
    VALUES (%s,%s)
    '''
    cursor.execute(q,x,i)
connection.commit()
print (cursor.fetchall())