import mysql.connector
from twitchio.ext import commands

connection = mysql.connector.connect(
    host = "192.168.1.3",
    port = "3306",
    user = "donuser",
    password = "ewq#@!",
    database = "donbon"
)
cursor = connection.cursor()

class Bot(commands.Bot):
#logowanie do IRC    
    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix = PREFIX, initial_channels=INITIAL_CHANNELS)  

    


connection.commit()
print (cursor.fetchall())