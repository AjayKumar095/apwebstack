from django.db import models
from core.models import Meta_Base, Row_Base
from django.core.validators import FileExtensionValidator
from core.models import Media

# Create your models here.


## Home page Meta tags
class Index_Meta(Meta_Base):
    pass
    class Meta:
        verbose_name = "Meta Data"
        verbose_name_plural = "Meta Data"  

## Home page hero section
class Hero_SectionIndex(models.Model):
    
    Heading = models.CharField(max_length=50, null=False, blank=False)
    Description = models.CharField(max_length=256, null=False, blank=False)
    
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="index_images"
    )
    img_alt = models.CharField( max_length=55, null=False, blank=False)
    
    def __str__(self):
        return f"{self.Heading}"
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

class Tech_LogoIndex(models.Model):
    logo_img = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tech_logo_images"
    )
    logo_alt = models.CharField( max_length=59, null=False, blank=False)
    
    def __str__(self):
        return f"{self.logo_alt}" 
    
    class Meta:
        verbose_name = "Tech Icon"
        verbose_name_plural = "Tech Icon"    
    
class WhyChooseUs_Index(models.Model):
    Heading = models.CharField(max_length=100, null=False, blank=False)
    Description = models.CharField(max_length=456, null=False, blank=False)
    
    def __str__(self):
        return f"{self.Heading}"
    
    class Meta:
        verbose_name = "Our Benefit" 
        verbose_name_plural = "Our Benefits"    
    
class WhyChooseUsRow_Index(Row_Base):
    section = models.ForeignKey(WhyChooseUs_Index, on_delete=models.CASCADE, related_name="whychooseus_rows_images")         
    
    
           
     
    


