from django.db import models


# -------------- CONTACT FORM MODEL ------------
class ContactForm(models.Model):
    
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=False, null=False)
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.email}"