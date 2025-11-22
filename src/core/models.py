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


# --------- ABSTRACT BASE MODELS ---------

class BulletPointBase(models.Model):
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True)
    icon_color = ColorField(default="#ae63e4")
    text = models.CharField(max_length=150)

    class Meta:
        abstract = True


class RowBase(models.Model):
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True)
    icon_color = ColorField(default="#ae63e4", null=True, blank=True)
    heading = models.CharField(max_length=55)
    paragraph = models.TextField(max_length=455)
    image = models.ImageField(upload_to="core/rows/", null=True, blank=True)
    image_alt = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True
    

