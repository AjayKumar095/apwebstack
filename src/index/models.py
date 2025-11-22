from django.db import models
from core.models import BulletPointBase, RowBase

# Create your models here.

## Home page hero section
class HeroSection(models.Model):
    
    Heading = models.CharField(max_length=50, null=False, blank=False)
    Description = models.CharField(max_length=260, null=False, blank=False)
    background_img = models.ImageField( upload_to="page/index/hero", null=False, blank=False)
    img_alt = models.CharField( max_length=55, null=False, blank=False)
    
    def __str__(self):
        return f"{self.Heading}"

class TechnologyLogo(models.Model):
    background_img = models.ImageField( upload_to="page/index/techlogo", null=False, blank=False)
    img_alt = models.CharField( max_length=55, null=False, blank=False)
    
    def __str__(self):
        return f"{self.img_alt}" 
    
class WhyChooseUs(models.Model):
    Heading = models.CharField(max_length=100, null=False, blank=False)
    Description = models.CharField(max_length=455, null=False, blank=False)
    
    def __str__(self):
        return f"{self.Heading}"
    
class WhyChooseUsRow(RowBase):
    section = models.ForeignKey(WhyChooseUs, on_delete=models.CASCADE, related_name="rows")         
    
    
           
     
    


