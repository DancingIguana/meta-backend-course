from django.db import models

# Create your models here.
class UserComments(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    comment = models.CharField(max_length=1000)