from django.db import models
from utils.icon_and_fonts import icons
from django.utils.text import slugify

# Create your models here.

class Add_Service(models.Model):
    
    icon = models.CharField(max_length=50, choices=icons)
    title = models.CharField(max_length=40, null=False, blank=False)
    short_description = models.CharField(max_length=170, null=False, blank=False)
    data_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Service_Sections(models.Model):
    pass