import pymysql


def get_connection():
    return pymysql.connect(host='localhost', user='asunawesker', password='yamaha112', db='hack_flask')