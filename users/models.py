import peewee as pw
from peewee_enum_field import EnumField
from ModelBase import Model
from enum import Enum

class UserType(Enum):
    COSTUMER="COSTUMER"
    VENDOR="VENDOR"
    VENUE_PROVIDER="VENUE_PROVIDER"
    STAFF="STAFF"
    


class Users(Model):
    id = pw.AutoField()
    username = pw.TextField()
    full_name = pw.TextField()
    email = pw.TextField()
    verification_code = pw.TextField()
    password_hash = pw.TextField()
    token = pw.TextField()
    user_type = EnumField(UserType)

    class Meta:
        table_name = 'users'
