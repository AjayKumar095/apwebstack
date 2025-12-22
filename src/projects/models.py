from django.db import models
from colorfield.fields import ColorField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings
import zipfile 
import shutil
import os

# Create your models here.

# ------------- DEMO PROJECT UPLOADER MODEL -----------------

MAX_ZIP_SIZE = 25 * 1024 * 1024  # 25 MB


def validate_zip_file(file):
    if not file.name.lower().endswith(".zip"):
        raise ValidationError("Only ZIP files are allowed.")

    if file.size > MAX_ZIP_SIZE:
        raise ValidationError("ZIP file must be under 25 MB")
    
def demo_zip_upload_path(instance, filename):
    name = slugify(instance.title)
    return f"uploads/demos/zips/{name}.zip"

class ProjectDemo(models.Model):

    CATEGORY_CHOICES = [
        ("business", "Business"),
        ("portfolio", "Portfolio"),
        ("blog", "Blog"),
        ("ecommerce", "E-Commerce"),
        ("landing", "Landing Page"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    zip_file = models.FileField(
        upload_to=demo_zip_upload_path,
        validators=[validate_zip_file]
    )

    project_path = models.CharField(
        max_length=500,
        blank=True,
        editable=False
    )

    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while ProjectDemo.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.zip_file:
            self.extract_zip()

    # -------------------------
    # SAFE ZIP EXTRACTION
    # -------------------------
    def extract_zip(self):
        zip_path = self.zip_file.path

        target_dir = os.path.join(
            settings.MEDIA_ROOT,
            "uploads",
            "demos",
            self.category,
            self.slug
        )

        os.makedirs(target_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                member_path = os.path.normpath(
                    os.path.join(target_dir, member)
                )
                if not member_path.startswith(os.path.abspath(target_dir)):
                    raise ValidationError("Unsafe ZIP file detected.")
            zip_ref.extractall(target_dir)

        # Save correct extracted path
        self.extracted_path = f"media/uploads/demos/{self.category}/{self.slug}/"
        super().save(update_fields=["project_path"])

        # Delete ZIP after extraction
        if os.path.exists(zip_path):
            os.remove(zip_path)

    # -------------------------
    # CLEANUP ON DELETE
    # -------------------------
    def delete(self, *args, **kwargs):
        demo_dir = os.path.join(
            settings.MEDIA_ROOT,
            "uploads",
            "demos",
            self.category,
            self.slug
        )

        if os.path.exists(demo_dir):
            shutil.rmtree(demo_dir)

        super().delete(*args, **kwargs)

    def __str__(self): 
        return self.title

    class Meta:
        verbose_name = "Upload Project"
        verbose_name_plural = "Upload Project"

        