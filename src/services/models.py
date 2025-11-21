from django.db import models
from django.utils.text import slugify
from core.models import Icon

# Create your models here.

class Add_Service(models.Model):
    
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True)
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
    
class Base(models.Model):
    
    heading = models.CharField(max_length=60)
    paragraph = models.CharField(max_length=500)
    
    class Mets:
        abstract = True
        
class Hero_Section(Base):
    
    data_Created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.heading
             
class Service_Details(Base):
    
    img = models.ImageField(blank=False)
    img_alt = models.CharField(max_length=25)
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True)     
          
    
    