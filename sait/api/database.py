import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="max",
        password="666315",
        database="mydb",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )