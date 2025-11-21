from django.db import models
from django.utils.text import slugify
from core.models import Icon, BulletPoint, Row
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

# --- SECTION 1: HERO SECTION ---
class ServiceHero(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="hero")
    heading = models.CharField(max_length=150)
    paragraph = models.TextField()

    def __str__(self):
        return f"Hero - {self.service.title}"


# --- SECTION 2: SERVICE DETAILS (with bullets) ---
class ServiceDetails(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="details")
    heading = models.CharField(max_length=150)
    paragraph = models.TextField()
    image = models.ImageField(upload_to="services/details/")
    image_alt = models.CharField(max_length=150)

    # Reuse BulletPoint model from core ✅
    bullets = models.ManyToManyField(BulletPoint, blank=True)

    def __str__(self):
        return f"Details - {self.service.title}"


# --- SECTION 3: SERVICE BENEFITS (with multiple rows) ---
class ServiceBenefits(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="benefits")
    heading = models.CharField(max_length=150)
    paragraph = models.TextField()
    image = models.ImageField(upload_to="services/benefits/", null=True, blank=True)
    image_alt = models.CharField(max_length=150, blank=True)

    # Reuse Row model ✅
    rows = models.ManyToManyField(Row, blank=True)

    def __str__(self):
        return f"Benefits - {self.service.title}"


# --- SECTION 4: WHY CHOOSE US ---
class WhyChooseUs(models.Model):
    service = models.OneToOneField(Add_Service, on_delete=models.CASCADE, related_name="why_choose")
    main_heading = models.CharField(max_length=150)
    short_paragraph = models.TextField()

    # Reuse Row model ✅
    rows = models.ManyToManyField(Row, blank=True)

    def __str__(self):
        return f"Why Choose Us - {self.service.title}"
