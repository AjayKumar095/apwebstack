from django.db import models
from colorfield.fields import ColorField
from django.core.validators import FileExtensionValidator
import os

def upload_to_extension_based(instance, filename):
    # extract extension
    ext = filename.split('.')[-1].lower()

    image_exts = ["png", "jpg", "jpeg", "webp", "svg"]
    doc_exts   = ["pdf", "doc", "docx"]
    obj_exts   = ["html", "css", "js"]

    if ext in image_exts:
        folder = "uploads/images"
    elif ext in doc_exts:
        folder = "uploads/docs"
    elif ext in obj_exts:
        folder = "uploads/obj"
    else:
        folder = "uploads/others"

    # final path returned to Django
    return os.path.join(folder, filename)


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
    
class Media(models.Model):
    file_name = models.CharField(max_length=100, unique=True, null=False)
    file = models.FileField(upload_to=upload_to_extension_based, max_length=255)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name}"
    
    @property
    def url(self):
        return self.file.url 

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"


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
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )
    image_alt = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True
    


class MetaBase(models.Model):
    meta_title = models.CharField(max_length=65)
    meta_description = models.CharField(max_length=160)
    meta_keywords = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Comma separated keywords"
    )
    canonical_url = models.URLField(blank=True, null=True)

    og_title = models.CharField(max_length=65, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    og_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    twitter_title = models.CharField(max_length=65, blank=True)
    twitter_description = models.CharField(max_length=160, blank=True)
    twitter_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    no_index = models.BooleanField(default=False)
    no_follow = models.BooleanField(default=False)

    class Meta:
        abstract = True   # ✅ Important for reuse
        verbose_name = "Meta Data"
        verbose_name_plural = "Meta Data"
        




