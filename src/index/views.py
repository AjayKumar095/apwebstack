from django.shortcuts import render
from django.core.cache import cache
from src.logger import log_error, log_info
from django.core.files.storage import default_storage
from .models import Hero_SectionIndex, WhyChooseUs_Index, Tech_LogoIndex, Index_Meta
from services.models import Add_Service


INDEX_CACHE_KEY = "index_page_data"
CACHE_TIMEOUT = 600  # 10 minutes


# -----------------------------------------------------
# HELPERS
# -----------------------------------------------------

def file_url(media_obj):
    """
    Safely return the file URL from a Media instance.
    """
    if not media_obj:
        return ""

    try:
        # Check file actually exists
        if default_storage.exists(media_obj.file.name):
            return media_obj.url  # because you created @property url
    except:
        pass

    return ""


def serialize_hero(hero):
    if not hero:
        return None

    return {
        "heading": hero.Heading,
        "description": hero.Description,
        "image": file_url(hero.image),
        "img_alt": hero.img_alt,
    }


def serialize_tech_logos(logos):
    return [
        {
            "image": file_url(obj.logo_img),
            "alt": obj.logo_alt
        }
        for obj in logos
    ]


def serialize_rows(rows):
    """Serialize Why Choose Us rows."""
    return [
        {
            "icon": row.icon.class_name if row.icon else None,
            "icon_color": row.icon_color,
            "heading": row.heading,
            "paragraph": row.paragraph,
            "image": file_url(row.image),
            "image_alt": row.image_alt,
        }
        for row in rows
    ]


def serialize_why_choose(section):
    if not section:
        return None

    return {
        "heading": section.Heading,
        "description": section.Description,
        "rows": serialize_rows(section.whychooseus_rows_images.all()),
    }


# -----------------------------------------------------
# VIEW
# -----------------------------------------------------

def index(request):
    log_info("Rendering Index Page")

    # -------------------------
    # 1. Try to load from Cache
    # -------------------------
    cached = cache.get(INDEX_CACHE_KEY)
    if cached:
        log_info("Data Source: Cache")
        #log_info(f"{cached}")
        return render(request, "index/index.html", {"index": cached})

    try:
        # -------------------------
        # 2. Load Fresh Data
        # -------------------------
        log_info("Data Source: Database (fresh load)")

        hero = Hero_SectionIndex.objects.select_related("image").first()

        why_choose = (
            WhyChooseUs_Index.objects
            .prefetch_related(
                "whychooseus_rows_images",
                "whychooseus_rows_images__icon",
                "whychooseus_rows_images__image",
            )
            .first()
        )

        logos = Tech_LogoIndex.objects.select_related("logo_img").all()

        services = (
            Add_Service.objects.select_related("icon")
            .only("title", "slug", "short_description", "icon__class_name")[:6]
        )

        meta = Index_Meta.objects.select_related(
            "og_image", "twitter_image"
        ).first()

        # -------------------------
        # 3. Serialize Data
        # -------------------------
        data = {
            "hero": serialize_hero(hero),
            "why_choose_us": serialize_why_choose(why_choose),
            "tech_logos": serialize_tech_logos(logos),

            "services": [
                {
                    "title": s.title,
                    "slug": s.slug,
                    "short_description": s.short_description,
                    "icon": s.icon.class_name if s.icon else "",
                }
                for s in services
            ],

            "meta": {
                "meta_title": meta.meta_title if meta else "",
                "meta_description": meta.meta_description if meta else "",
                "meta_keywords": meta.meta_keywords if meta else "",
                "canonical_url": meta.canonical_url if meta else "",

                "og_title": meta.og_title if meta else "",
                "og_description": meta.og_description if meta else "",
                "og_image": meta.og_image.url if meta and meta.og_image else "",

                "twitter_title": meta.twitter_title if meta else "",
                "twitter_description": meta.twitter_description if meta else "",
                "twitter_image": meta.twitter_image.url if meta and meta.twitter_image else "",

                "no_index": meta.no_index if meta else False,
                "no_follow": meta.no_follow if meta else False,
            }
        }

        # -------------------------
        # 4. Save to Cache
        # -------------------------
        cache.set(INDEX_CACHE_KEY, data, CACHE_TIMEOUT)
        #log_info(f"{data}")
        return render(request, "index/index.html", {"index": data})

    except Exception as e:
        log_error(f"Error rendering index: {e}")

        return render(
            request,
            "error/errors.html",
            {
                "status": 500,
                "error": "Server Error",
                "message": "Something went wrong while loading the page.",
            },
            status=500
        )
