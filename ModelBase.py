import peewee as pw
from setting import MYSQL_USER, MYSQL_DATABASE, MYSQLHOST, MYSQLPASSWORD, MYSQLPORT

db = pw.MySQLDatabase(
    MYSQL_DATABASE,
    host=MYSQLHOST,
    user=MYSQL_USER,
    password=MYSQLPASSWORD,
    connect_timeout=3600
)

class Model(pw.Model):
    class Meta:
        database = db
