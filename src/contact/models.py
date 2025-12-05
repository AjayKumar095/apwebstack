from django.db import models
from core.models import Meta_Base


# -------------- CONTACT FORM MODEL ------------

class Contact_Meta(Meta_Base):
    pass

class Contact_Form(models.Model):
    
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=259, blank=False, null=False)
    message = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        verbose_name = "Contact Form"
        verbose_name_plural = "Contact Form"
    
