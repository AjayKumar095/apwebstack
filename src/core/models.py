from django.db import models
from colorfield.fields import ColorField
from django.core.validators import FileExtensionValidator


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
    image = models.FileField(upload_to="core/rows/", null=True, blank=True,
                                            validators=[FileExtensionValidator(
                                            allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'svg'],
                                       )])
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
    og_image = models.ImageField(upload_to="seo/og/", blank=True, null=True)

    twitter_title = models.CharField(max_length=65, blank=True)
    twitter_description = models.CharField(max_length=160, blank=True)
    twitter_image = models.ImageField(upload_to="seo/twitter/", blank=True, null=True)

    no_index = models.BooleanField(default=False)
    no_follow = models.BooleanField(default=False)

    class Meta:
        abstract = True   # ✅ Important for reuse

