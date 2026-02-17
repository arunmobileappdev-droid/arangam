from django.db import models

class UserDetail(models.Model):

    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.user_name
