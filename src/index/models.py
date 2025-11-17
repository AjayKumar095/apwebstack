from django.db import models

# Create your models here.

## Home page hero section
class HeroSection(models.Model):
    
    Heading = models.CharField(max_length=50, null=False, blank=False)
    Description = models.CharField(max_length=260, null=False, blank=False)
    Date_Created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        get_latest_by = 'Data_Created'
    

