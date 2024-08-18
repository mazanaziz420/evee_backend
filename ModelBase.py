import peewee as pw
from setting import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DATABASE, POSTGRES_HOST, POSTGRES_PORT

db = pw.PostgresqlDatabase(
    POSTGRES_DATABASE,
    host=POSTGRES_HOST,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT,
    connect_timeout=3600
)

class Model(pw.Model):
    class Meta:
        database = db
