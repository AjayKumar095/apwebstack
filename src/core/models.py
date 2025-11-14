from django.db import models

# Create your models here.

class MetaData(models.Model):
    meta_title = models.TextField(max_length=60, editable=True, blank=False)
    meta_description = models.TextField(max_length=156, editable=True, blank=False)
    
    # class Meta:
    #     abstract = True

