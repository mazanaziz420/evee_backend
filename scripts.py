import peewee as pw
from setting import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DATABASE, POSTGRES_HOST, POSTGRES_PORT
from enum import Enum

# Define the database connection
db = pw.PostgresqlDatabase(
    POSTGRES_DATABASE,
    host=POSTGRES_HOST,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT
)

# Define the UserType Enum
class UserType(Enum):
    COSTUMER = "COSTUMER"
    VENDOR = "VENDOR"
    VENUE_PROVIDER = "VENUE_PROVIDER"
    STAFF = "STAFF"

# Define the Users model
class Users(pw.Model):
    id = pw.AutoField()
    username = pw.TextField(unique=True)
    full_name = pw.TextField()
    email = pw.TextField(unique=True)
    verification_code = pw.TextField()
    password_hash = pw.TextField()
    token = pw.TextField(null=True)
    user_type = pw.CharField()  # Use CharField for Enum

    class Meta:
        database = db
        table_name = 'users'

def create_tables():
    with db:
        # Create the users table if it does not exist
        db.create_tables([Users])

if __name__ == '__main__':
    create_tables()
