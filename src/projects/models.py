from django.db import models, transaction
from django.core.exceptions import ValidationError
from core.models import Media
from django.utils.text import slugify
from django.conf import settings
from pathlib import Path
import zipfile 
import shutil
import os
from uuid import uuid4


# ------------- DEMO PROJECT UPLOADER MODEL -----------------

MAX_ZIP_SIZE = 25 * 1024 * 1024  # 25 MB


def validate_zip_file(file):
    if not file.name.lower().endswith(".zip"):
        raise ValidationError("Only ZIP files are allowed.")

    # MIME validation (extra safety)
    if hasattr(file, "content_type"):
        if file.content_type not in ["application/zip", "application/x-zip-compressed"]:
            raise ValidationError("Invalid ZIP file type.")

    if file.size > MAX_ZIP_SIZE:
        raise ValidationError("ZIP file must be under 25 MB")
    

def demo_zip_upload_path(instance, filename):
    name = slugify(instance.title)
    return f"uploads/demos/zips/{name}-{uuid4().hex}.zip"


class ProjectDemo(models.Model):
    
    BUSINESS = "Business"
    PORTFOLIO = "Portfolio"
    BLOG = "Blog"
    ECOMMERCE = "E-Commerce"
    LANDING = "Landing-Page"
    
    CATEGORY_CHOICES = (
        (BUSINESS, "Business"),
        (PORTFOLIO, "Portfolio"),
        (BLOG, "Blog"),
        (ECOMMERCE, "E-Commerce"),
        (LANDING, "Landing-Page"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    thumbnail = models.ForeignKey(Media, null=True, blank=True, on_delete=models.SET_NULL)
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
            with transaction.atomic():
                self.extract_zip()

    # -------------------------
    # SAFE ZIP EXTRACTION
    # -------------------------
    def extract_zip(self):
        zip_path = self.zip_file.path

        safe_category = slugify(self.category)

        target_dir = os.path.join(
            settings.MEDIA_ROOT,
            "uploads",
            "demos",
            safe_category,
            self.slug
        )

        os.makedirs(target_dir, exist_ok=True)

        index_html_path = None

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            members = zip_ref.namelist()

            # Detect single root folder
            root_dirs = {
                m.split("/")[0]
                for m in members
                if "/" in m
            }

            for member in members:
                if member.endswith("/"):
                    continue

                source_name = member

                # Remove root folder if zip has only one
                if len(root_dirs) == 1 and "/" in member:
                    member = member.split("/", 1)[1]

                dest_path = os.path.normpath(
                    os.path.join(target_dir, member)
                )

                # ---- ZIP SLIP PROTECTION (SECURE) ----
                if not os.path.commonpath([
                    os.path.abspath(dest_path),
                    os.path.abspath(target_dir)
                ]) == os.path.abspath(target_dir):
                    raise ValidationError("Unsafe ZIP file detected.")

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                with zip_ref.open(source_name) as src, open(dest_path, "wb") as dst:
                    shutil.copyfileobj(src, dst)

                if member.lower().endswith("index.html"):
                    index_html_path = dest_path

        if not index_html_path:
            raise ValidationError("ZIP must contain an index.html file")

        # -------- SAVE WEB-SAFE RELATIVE PATH --------
        media_root = Path(settings.MEDIA_ROOT)
        self.project_path = str(
            Path(index_html_path).relative_to(media_root)
        ).replace(os.sep, "/")   # 🔥 critical fix

        super().save(update_fields=["project_path"])

        # Delete ZIP only after full success
        if os.path.exists(zip_path):
            os.remove(zip_path)

    # -------------------------
    # CLEANUP ON DELETE
    # -------------------------
    def delete(self, *args, **kwargs):
        if self.project_path:
            demo_dir = os.path.dirname(
                os.path.join(settings.MEDIA_ROOT, self.project_path)
            )

            if os.path.exists(demo_dir):
                shutil.rmtree(demo_dir, ignore_errors=True)

        super().delete(*args, **kwargs)

    def __str__(self): 
        return self.title

    class Meta:
        verbose_name = "Upload Project"
        verbose_name_plural = "Upload Project"