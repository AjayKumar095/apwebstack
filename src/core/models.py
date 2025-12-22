from django.db import models
from colorfield.fields import ColorField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings
import zipfile 
import shutil
import os

def upload_to_extension_based(instance, filename):
    # extract extension
    ext = filename.split('.')[-1].lower()

    image_exts = ["png", "jpg", "jpeg", "webp", "svg"]
    doc_exts   = ["pdf", "doc", "docx"]
    obj_exts   = ["html", "css", "js"]

    if ext in image_exts:
        folder = "uploads/images"
    elif ext in doc_exts:
        folder = "uploads/docs"
    elif ext in obj_exts:
        folder = "uploads/obj"
    else:
        folder = "uploads/others"

    # final path returned to Django
    return os.path.join(folder, filename)


# Create your models here.

class Icon(models.Model):
    """
    Admin can add bootstrap icon's in this model, this model store the icon name and bootstrap 
    icon class name.
    """
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.class_name}"
    
class Media(models.Model):
    file_name = models.CharField(max_length=100, unique=True, null=False)
    file = models.FileField(upload_to=upload_to_extension_based, max_length=255)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name}"
    
    @property
    def url(self):
        return self.file.url 

    class Meta:
        verbose_name = "Media File"
        verbose_name_plural = "Media File"

# --------- ABSTRACT BASE MODELS ---------

class Bullet_PointBase(models.Model):
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True)
    icon_color = ColorField(default="#ae63e4", null=True, blank=True)
    text = models.CharField(max_length=150)

    class Meta:
        abstract = True


class Row_Base(models.Model):
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True)
    icon_color = ColorField(default="#ae63e4", null=True, blank=True)
    heading = models.CharField(max_length=55)
    paragraph = models.TextField(max_length=455)
    image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )
    image_alt = models.CharField(max_length=256, blank=True)

    class Meta:
        abstract = True
    

class Meta_Base(models.Model):
    meta_title = models.CharField(max_length=65)
    meta_description = models.CharField(max_length=159)
    meta_keywords = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Comma separated keywords"
    )
    canonical_url = models.URLField(blank=True, null=True)

    og_title = models.CharField(max_length=65, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    og_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    twitter_title = models.CharField(max_length=65, blank=True)
    twitter_description = models.CharField(max_length=160, blank=True)
    twitter_image = models.ForeignKey(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )

    no_index = models.BooleanField(default=False)
    no_follow = models.BooleanField(default=False)

    class Meta:
        abstract = True   # ✅ Important for reuse
        verbose_name = "Meta Data"
        verbose_name_plural = "Meta Data"
        

# ------------- DEMO PROJECT UPLOADER MODEL -----------------

# MAX_ZIP_SIZE = 25 * 1024 * 1024  # 25 MB


# def validate_zip_file(file):
#     if not file.name.lower().endswith(".zip"):
#         raise ValidationError("Only ZIP files are allowed.")

#     if file.size > MAX_ZIP_SIZE:
#         raise ValidationError("ZIP file must be under 25 MB
# def demo_zip_upload_path(instance, filename):
#     name = slugify(instance.title)
#     return f"uploads/demos/zips/{name}.zip"

# class ProjectDemo(models.Model):

#     CATEGORY_CHOICES = [
#         ("business", "Business"),
#         ("portfolio", "Portfolio"),
#         ("blog", "Blog"),
#         ("ecommerce", "E-Commerce"),
#         ("landing", "Landing Page"),
#     ]

#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True, blank=True)
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

#     zip_file = models.FileField(
#         upload_to=demo_zip_upload_path,
#         validators=[validate_zip_file]
#     )

#     project_path = models.CharField(
#         max_length=500,
#         blank=True,
#         editable=False
#     )

#     is_active = models.BooleanField(default=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     # -------------------------
#     # SAVE
#     # -------------------------
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             base_slug = slugify(self.title)
#             slug = base_slug
#             count = 1
#             while ProjectDemo.objects.filter(slug=slug).exists():
#                 slug = f"{base_slug}-{count}"
#                 count += 1
#             self.slug = slug

#         is_new = self.pk is None
#         super().save(*args, **kwargs)

#         if is_new and self.zip_file:
#             self.extract_zip()

#     # -------------------------
#     # SAFE ZIP EXTRACTION
#     # -------------------------
#     def extract_zip(self):
#         zip_path = self.zip_file.path

#         target_dir = os.path.join(
#             settings.MEDIA_ROOT,
#             "uploads",
#             "demos",
#             self.category,
#             self.slug
#         )

#         os.makedirs(target_dir, exist_ok=True)

#         with zipfile.ZipFile(zip_path, "r") as zip_ref:
#             for member in zip_ref.namelist():
#                 member_path = os.path.normpath(
#                     os.path.join(target_dir, member)
#                 )
#                 if not member_path.startswith(os.path.abspath(target_dir)):
#                     raise ValidationError("Unsafe ZIP file detected.")
#             zip_ref.extractall(target_dir)

#         # Save correct extracted path
#         self.extracted_path = f"media/uploads/demos/{self.category}/{self.slug}/"
#         super().save(update_fields=["extracted_path"])

#         # Delete ZIP after extraction
#         if os.path.exists(zip_path):
#             os.remove(zip_path)

#     # -------------------------
#     # CLEANUP ON DELETE
#     # -------------------------
#     def delete(self, *args, **kwargs):
#         demo_dir = os.path.join(
#             settings.MEDIA_ROOT,
#             "uploads",
#             "demos",
#             self.category,
#             self.slug
#         )

#         if os.path.exists(demo_dir):
#             shutil.rmtree(demo_dir)

#         super().delete(*args, **kwargs)

#     def __str__(self): 
#         return self.title

#     class Meta:
#         verbose_name = "Upload Project"
#         verbose_name_plural = "Upload Project"

        