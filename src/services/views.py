from django.shortcuts import get_object_or_404, render
from src.logger import log_error, log_info
from django.core.cache import cache
from .models import (
    Add_Service,
)

def serialize_service(service):
    """
    Convert service and related sections to pure Python types (dicts/lists).
    """
    # basic service
    data = {
        "id": service.id,
        "title": service.title,
        "short_description": service.short_description,
        "slug": service.slug,
        "icon": service.icon.class_name if service.icon else None,
        "data_created": service.data_created.isoformat() if service.data_created else None,
    }

    # hero (OneToOne)
    hero = getattr(service, "hero", None)
    if hero:
        data["hero"] = {
            "heading": hero.heading,
            "paragraph": hero.paragraph,
        }
    else:
        data["hero"] = None

    # details (OneToOne) + bullets (related)
    details = getattr(service, "details", None)
    if details:
        bullets = []
        for b in details.bullets.all():
            bullets.append({
                "id": b.id,
                "text": b.text,
                "icon": b.icon.class_name if b.icon else None,
                "icon_color": getattr(b, "icon_color", None)
            })

        data["details"] = {
            "heading": details.heading,
            "paragraph": details.paragraph,
            "image": details.image.url if details.image else None,
            "image_alt": details.image_alt,
            "bullets": bullets
        }
    else:
        log_error("Error while serializing service details: Details section is missing.")
        data["details"] = None

    # benefits + rows
    benefits = getattr(service, "benefits", None)
    if benefits:
        rows = []
        for r in benefits.rows.all():
            rows.append({
                "id": r.id,
                "heading": r.heading,
                "paragraph": r.paragraph,
                "icon": r.icon.class_name if r.icon else None,
                "icon_color": getattr(r, "icon_color", None),
                "image": r.image.url if r.image else None,
                "image_alt": r.image_alt
            })

        data["benefits"] = {
            "heading": benefits.heading,
            "paragraph": benefits.paragraph,
            "image": benefits.image.url if benefits.image else None,
            "image_alt": benefits.image_alt,
            "rows": rows
        }
    else:
        data["benefits"] = None

    # why choose + rows
    why = getattr(service, "why_choose", None)
    if why:
        why_rows = []
        for r in why.rows.all():
            why_rows.append({
                "id": r.id,
                "heading": r.heading,
                "paragraph": r.paragraph,
                "icon": r.icon.class_name if r.icon else None,
                "icon_color": getattr(r, "icon_color", None),
                "image": r.image.url if r.image else None,
                "image_alt": r.image_alt
            })

        data["why_choose"] = {
            "main_heading": why.main_heading,
            "short_paragraph": why.short_paragraph,
            "rows": why_rows
        }
    else:
        data["why_choose"] = None

    return data


def service_detail(request, slug):
    
    try:
        log_info(f"Rendering Service Page for slug: {slug}")
        cache_key = f"service_detail_{slug}"

        # Try cache first
        cached = cache.get(cache_key)
        if cached is not None:
            log_info('Data Source (service page): cached')
            return render(request, "service/service.html", {"service": cached})

        # Not in cache -> fetch from DB using optimized queries
        service = get_object_or_404(
            Add_Service.objects.select_related(
                "icon",
                # OneToOne relations are accessed directly; select_related helps if they exist
                # but if OneToOne objects are missing, select_related still safe
                "hero",
                "details",
                "benefits",
                "why_choose"
            ).prefetch_related(
                "details__bullets",
                "benefits__rows",
                "why_choose__rows"
            ),
            slug=slug
        )

    # Serialize to pure python types
        data = serialize_service(service)

        # Save serialized data to cache (stored indefinitely until invalidated)
        cache.set(cache_key, data, timeout=3600)  # use None or 0 depends on backend; None usually means no expiry
        log_info('Data Source (service app): Database')
        return render(request, "service/service.html", {"service": data})
    
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
