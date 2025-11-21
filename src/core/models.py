from django.db import models
from colorfield.fields import ColorField

# Create your models here.

class Icon(models.Model):
    """
    Admin can add bootstrap icon's in this model, this model store the icon name and bootstrap 
    icon class name.
    """
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.class_name}"


class Bullets_Point(models.Model):
    
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True)  
    icon_color = ColorField(default="#ae63e4")
    text = models.CharField(max_length=150)
    
    
    