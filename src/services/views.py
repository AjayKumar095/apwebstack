from django.shortcuts import get_object_or_404, render
from django.core.cache import cache
from src.logger import log_error, log_info

from .models import (
    Add_Service,
    Service_Hero,
    Service_Details,
    Service_DetailBullet,
    Service_Benefits,
    Service_BenefitRow,
    WhyChoose_Us,
    WhyChooseUsRow,
    Service_Meta,
)


def serialize_service(service):
    """Convert full service data into a clean serialized dict."""

    data = {
        "id": service.id,
        "title": service.title,
        "short_description": service.short_description,
        "slug": service.slug,
        "icon": service.icon.class_name if service.icon else None,
        "date_created": service.data_created.isoformat() if service.data_created else None,
    }

    # ---- HERO ----
    hero = getattr(service, "service_hero", None)
    data["hero"] = {
        "heading": hero.heading,
        "paragraph": hero.paragraph
    } if hero else None

    # ---- DETAILS + BULLETS ----
    details = getattr(service, "service_details", None)
    if details:
        bullets = [
            {
                "id": bullet.id,
                "text": bullet.text,
                "icon": bullet.icon.class_name if bullet.icon else None,
                "icon_color": bullet.icon_color,
            }
            for bullet in details.service_bullets.all()
        ]

        data["details"] = {
            "heading": details.heading,
            "paragraph": details.paragraph,
            "image": details.image.url if details.image else None,
            "image_alt": details.image_alt,
            "bullets": bullets,
        }
    else:
        data["details"] = None

    # ---- BENEFITS ----
    benefits = getattr(service, "service_benefits", None)
    if benefits:
        rows = [
            {
                "id": row.id,
                "heading": row.heading,
                "paragraph": row.paragraph,
                "icon": row.icon.class_name if row.icon else None,
                "icon_color": row.icon_color,
                "image": row.image.url if row.image else None,
                "image_alt": row.image_alt,
            }
            for row in benefits.service_rows.all()
        ]

        data["benefits"] = {
            "heading": benefits.heading,
            "paragraph": benefits.paragraph,
            "image": benefits.image.url if benefits.image else None,
            "image_alt": benefits.image_alt,
            "rows": rows,
        }
    else:
        data["benefits"] = None

    # ---- WHY CHOOSE US ----
    why = getattr(service, "why_choose_service", None)
    if why:
        rows = [
            {
                "id": row.id,
                "heading": row.heading,
                "paragraph": row.paragraph,
                "icon": row.icon.class_name if row.icon else None,
                "icon_color": row.icon_color,
                "image": row.image.url if row.image else None,
                "image_alt": row.image_alt,
            }
            for row in why.whychoose_service_rows.all()
        ]

        data["why_choose"] = {
            "main_heading": why.main_heading,
            "short_paragraph": why.short_paragraph,
            "rows": rows,
        }
    else:
        data["why_choose"] = None

    # ---- META ----
    meta = getattr(service, "service_meta", None)
    if meta:
        data["meta"] = {
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "meta_keywords": meta.meta_keywords,
            "canonical_url": meta.canonical_url,

            "og_title": meta.og_title,
            "og_description": meta.og_description,
            "og_image": meta.og_image.url if meta.og_image else None,

            "twitter_title": meta.twitter_title,
            "twitter_description": meta.twitter_description,
            "twitter_image": meta.twitter_image.url if meta.twitter_image else None,

            "no_index": meta.no_index,
            "no_follow": meta.no_follow,
        }
    else:
        data["meta"] = None
   
    return data



def service_detail(request, slug):
    """Render the service detail page."""

    try:
        log_info(f"Rendering service page for slug: {slug}")

        cache_key = f"service_page_{slug}"
        cached = cache.get(cache_key)

        if cached:
            log_info("Service page served from cache")
            return render(request, "service/service.html", {"service": cached})

        # -------- QUERY OPTIMIZED --------
        service = get_object_or_404(
            Add_Service.objects
            .select_related(
                "icon",
                "service_hero",
                "service_details",
                "service_benefits",
                "why_choose_service",
                "service_meta",
            )
            .prefetch_related(
                "service_details__service_bullets",
                "service_benefits__service_rows",
                "why_choose_service__whychoose_service_rows",
            ),
            slug=slug
        )

        data = serialize_service(service)

        # store in cache 1 hour
        cache.set(cache_key, data, timeout=3600)

        log_info("Service page served from database")

        return render(request, "service/service.html", {"service": data})

    except Exception as e:
        log_error(f"Service Page Error: {e}")

        return render(
            request,
            "error/errors.html",
            {
                "status": 404,
                "error": "Page Not Found",
                "message": "Sorry, the service you are looking for does not exist.",
                "page": "services"
            },
            status=404
        )
