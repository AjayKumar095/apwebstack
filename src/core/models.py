from django.db import models

# Create your models here.

class Icon(models.Model):
    """
    Admin can add bootstrap icon's in this model, this model store the icon name and bootstrap 
    icon class name.
    """
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.class_name}"


class SectionType(models.Model):
    """
    Admin can create section types here and choose which fields
    are used for that section (so no hard-coded section types).
    """
    name = models.CharField(max_length=120, unique=True)

    # field flags — control which inputs a section shows/uses
    use_heading = models.BooleanField(default=True)
    use_paragraph = models.BooleanField(default=True)
    use_image = models.BooleanField(default=False)
    use_image_alt = models.BooleanField(default=False)
    use_icon = models.BooleanField(default=False)
    use_bullets = models.BooleanField(default=False)
    use_rows = models.BooleanField(default=False)

    def __str__(self):
        return self.name