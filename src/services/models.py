from django.db import models
from django.utils.text import slugify
from core.models import Icon, BulletPointBase, RowBase
from colorfield.fields import ColorField



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

# ---------- HERO ----------
class ServiceHero(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="hero")
    heading = models.CharField(max_length=150)
    paragraph = models.TextField()

    def __str__(self):
        return f"Hero - {self.service.title}"


# ---------- DETAILS ----------
class ServiceDetails(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="details")
    heading = models.CharField(max_length=150)
    paragraph = models.TextField()
    image = models.ImageField(upload_to="services/media/details/")
    image_alt = models.CharField(max_length=150)

    def __str__(self):
        return f"Details - {self.service.title}"


class ServiceDetailBullet(BulletPointBase):
    section = models.ForeignKey(ServiceDetails, on_delete=models.CASCADE, related_name="bullets")

    def __str__(self):
        return self.text


# ---------- BENEFITS ----------
class ServiceBenefits(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="benefits")
    heading = models.CharField(max_length=150)
    paragraph = models.TextField()
    image = models.ImageField(upload_to="services/media/benefits/", null=True, blank=True)
    image_alt = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Benefits - {self.service.title}"


class ServiceBenefitRow(RowBase):
    section = models.ForeignKey(ServiceBenefits, on_delete=models.CASCADE, related_name="rows")

    def __str__(self):
        return self.heading


# ---------- WHY CHOOSE ----------
class WhyChooseUs(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="why_choose")
    main_heading = models.CharField(max_length=150)
    short_paragraph = models.TextField()

    def __str__(self):
        return f"Why Choose - {self.service.title}"


class WhyChooseUsRow(RowBase):
    section = models.ForeignKey(WhyChooseUs, on_delete=models.CASCADE, related_name="rows")

    def __str__(self):
        return self.heading