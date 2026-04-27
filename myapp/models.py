from django.db import models

# Create your models here.
class students(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name