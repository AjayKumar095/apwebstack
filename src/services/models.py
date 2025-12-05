from django.db import models
from django.utils.text import slugify
from core.models import Icon, Bullet_PointBase, Row_Base, Meta_Base
from django.core.validators import FileExtensionValidator
from core.models import Media




# Create your models here.
class Service_Meta(Meta_Base):
    service = models.OneToOneField(
        "services.Add_Service",
        on_delete=models.CASCADE,
        related_name="service_meta"
    )
 
    class Meta:
        verbose_name = "Meta Data"
        verbose_name_plural = "Meta Data"     

class Add_Service(models.Model):
    
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, related_name="icon")
    title = models.CharField(max_length=40, null=False, blank=False)
    short_description = models.CharField(max_length=179, null=False, blank=False)
    data_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Add Service"
        verbose_name_plural = "Add Service" 

# ---------- HERO ----------
class Service_Hero(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="service_hero")
    heading = models.CharField(max_length=159)
    paragraph = models.TextField()

    def __str__(self):
        return f"Hero - {self.service.title}"
    
    class Meta:
        verbose_name = "Header"
        verbose_name_plural = "Header"     


# ---------- DETAILS ----------
class Service_Details(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="service_details")
    heading = models.CharField(max_length=159)
    paragraph = models.TextField()
    
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_details_images"
    )
    image_alt = models.CharField(max_length=150)

    def __str__(self):
        return f"Details - {self.service.title}"

    class Meta:
        verbose_name = "Details"
        verbose_name_plural = "Details"     


class Service_DetailBullet(Bullet_PointBase):
    section = models.ForeignKey(Service_Details, on_delete=models.CASCADE, related_name="service_bullets")

    def __str__(self):
        return self.text


# ---------- BENEFITS ----------
class Service_Benefits(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="service_benefits")
    heading = models.CharField(max_length=159)
    paragraph = models.TextField()
   
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_benefits_images"
    )
    image_alt = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Benefits - {self.service.title}"
    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefit"     


class Service_BenefitRow(Row_Base):
    section = models.ForeignKey(Service_Benefits, on_delete=models.CASCADE, related_name="service_rows")

    def __str__(self):
        return self.heading


# ---------- WHY CHOOSE ----------
class WhyChoose_Us(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="why_choose_service")
    main_heading = models.CharField(max_length=15)
    short_paragraph = models.TextField()

    def __str__(self):
        return f"Why Choose - {self.service.title}"
    
    class Meta:
        verbose_name = "Our Service"
        verbose_name_plural = "Our Service"     


class WhyChooseUsRow(Row_Base):
    section = models.ForeignKey(WhyChoose_Us, on_delete=models.CASCADE, related_name="whychoose_service_rows")

    def __str__(self):
        return self.heading