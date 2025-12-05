from django.shortcuts import render
from django.core.cache import cache
from src.logger import log_error, log_info

from .models import Hero_SectionIndex, WhyChooseUs_Index, Tech_LogoIndex, Index_Meta
from services.models import Add_Service


# -----------------------------------------------------
#  HELPERS
# -----------------------------------------------------

def file_url(field):
    """Safe file field to URL."""
    return field.url if field and hasattr(field, "url") else ""


def serialize_hero(hero):
    if not hero:
        return None

    return {
        "heading": hero.Heading,
        "description": hero.Description,
        "background_img": file_url(hero.background_img),
        "img_alt": hero.img_alt,
    }


def serialize_tech_logos(logos):
    return [
        {
            "image": file_url(l.logo_img),
            "alt": l.logo_alt
        }
        for l in logos
    ]


def serialize_rows(rows):
    return [
        {
            "icon": r.icon.class_name if r.icon else None,
            "icon_color": r.icon_color,
            "heading": r.heading,
            "paragraph": r.paragraph,
            "image": file_url(r.image),
            "image_alt": r.image_alt,
        }
        for r in rows
    ]


def serialize_why_choose(section):
    if not section:
        return None

    return {
        "heading": section.Heading,
        "description": section.Description,
        "rows": serialize_rows(section.rows.all()),
    }


# -----------------------------------------------------
#  VIEW
# -----------------------------------------------------

def index(request):
    log_info("Rendering Index Page")
    # cache_key = "index_page_data"

    # # --- 1. Try cache ---
    # if (cached := cache.get(cache_key)) is not None:
    #     log_info("Data Source: Cached")
    #     #log_info(f"{cached}")
    #     return render(request, "index/index.html", {"index": cached})

    try:
    #     # --- 2. DB Queries (Optimized) ---
    #     hero = Hero_SectionIndex.objects.only(
    #         "Heading", "Description", "background_img", "img_alt"
    #     ).first()

    #     why_choose = (
    #         WhyChooseUs_Index.objects.prefetch_related("rows", "rows__icon")
    #         .only("Heading", "Description")
    #         .first()
    #     )

    #     logos = Tech_LogoIndex.objects.only("logo_img", "logo_alt")

    #     services = (
    #         Add_Service.objects.select_related("icon")
    #         .only("title", "slug", "short_description", "icon__class_name")
    #         [:6]
    #     )

    #     # --- 3. Serialize ---
    #     meta = Index_Meta.objects.first()
    #     data = {
    #         "hero": serialize_hero(hero),
    #         "why_choose_us": serialize_why_choose(why_choose),
    #         "tech_logos": serialize_tech_logos(logos),
    #         "services": [
    #                 {
    #                     "title": s.title,
    #                     "slug": s.slug,
    #                     "short_description": s.short_description,
    #                     "icon": s.icon.class_name if s.icon else "",
    #                 }
    #                 for s in services
    #             ] ,
    #         "meta": {
    #     # Meta fields
    #     "meta_title": meta.meta_title if meta else "sample title",
    #     "meta_description": meta.meta_description if meta else "",
    #     "meta_keywords": meta.meta_keywords if meta else "",
    #     "canonical_url": meta.canonical_url if meta else "",

    #     "og_title": meta.og_title if meta else "",
    #     "og_description": meta.og_description if meta else "",
    #     "og_image": meta.og_image.url if meta and meta.og_image else "",

    #     "twitter_title": meta.twitter_title if meta else "",
    #     "twitter_description": meta.twitter_description if meta else "",
    #     "twitter_image": meta.twitter_image.url if meta and meta.twitter_image else "",

    #     "no_index": meta.no_index if meta else False,
    #     "no_follow": meta.no_follow if meta else False,
    # }
                           
    #     }

    #     # --- 4. Save to cache ---
    #     cache.set(cache_key, data, timeout=3600)
    #     log_info("Data Source: Database")
    #     #log_info(f"{data}") , {"index": data}
        return render(request, "index/index.html")

    except Exception as e:
        context = {
            "status": 404,
            "error": "Page Not Found",
            "message": "Sorry, the page you are looking for doesn’t exist or may have been moved.",
            "page": "index"
        }

        log_error(
            f"Error occurred while rendering index page.\n"
            f"Exception: {type(e).__name__}\n"
            f"Message: {e}"
        )

        return render(
            request=request,
            template_name="error/errors.html",
            context=context,
            status=404
        )
