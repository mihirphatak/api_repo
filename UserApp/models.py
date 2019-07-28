from django.db import models

# Create your models here.
class User(models.Model):
    USER_TYPE_MODERATOR = 1
    USER_TYPE_APP_USER = 2

    USER_TYPE_CHOICES = (
        (USER_TYPE_MODERATOR, 'Moderator'),
        (USER_TYPE_APP_USER, 'App User'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=USER_TYPE_APP_USER)
    contact_number = models.CharField(max_length=10, unique=True, db_index=True)
    first_name = models.CharField(max_length=10, null=True)
    last_name = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.contact_number

    class FieldNames:
        user_type = "user_type"
        contact_number = "contact_number"
        first_name = "first_name"
        last_name = "last_name"
        email = "email"
        password = "password"