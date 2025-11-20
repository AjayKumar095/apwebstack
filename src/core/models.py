from django.db import models

# Create your models here.

class Icon(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.class_name}"
