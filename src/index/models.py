from django.db import models
from core.models import BulletPointBase, RowBase
from django.core.validators import FileExtensionValidator

# Create your models here.

## Home page hero section
class HeroSectionIndex(models.Model):
    
    Heading = models.CharField(max_length=50, null=False, blank=False)
    Description = models.CharField(max_length=260, null=False, blank=False)
    background_img = models.FileField( upload_to="page/index/hero", null=False, blank=False,
                                       validators=[FileExtensionValidator(
                                            allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'svg'],
                                            message="Upload a valid image. The file you uploaded was either not an image or a corrupted image. ['jpg', 'jpeg', 'png', 'webp']"
                                       )])
    img_alt = models.CharField( max_length=55, null=False, blank=False)
    
    def __str__(self):
        return f"{self.Heading}"

class TechnologyLogoIndex(models.Model):
    logo_img = models.FileField( upload_to="page/index/techlogo", null=False, blank=False,
                                            validators=[FileExtensionValidator(
                                            allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'svg'],
                                       )])
    logo_alt = models.CharField( max_length=55, null=False, blank=False)
    
    def __str__(self):
        return f"{self.logo_alt}" 
    
class WhyChooseUsIndex(models.Model):
    Heading = models.CharField(max_length=100, null=False, blank=False)
    Description = models.CharField(max_length=455, null=False, blank=False)
    
    def __str__(self):
        return f"{self.Heading}"
    
class WhyChooseUsRowIndex(RowBase):
    section = models.ForeignKey(WhyChooseUsIndex, on_delete=models.CASCADE, related_name="rows")         
    
    
           
     
    


