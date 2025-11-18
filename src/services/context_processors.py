import logging
from .models import Add_Service

logger = logging.getLogger(__name__)

def navbar_services(request):
    try:
        services = Add_Service.objects.only(
            "icon", "title", "slug"
        ).order_by("title")

        return {"navbar_services": services}

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Navbar Service Error: {e}")

        # Fallback service (safe default)
        fallback = [
            {
                "icon": "bi bi-exclamation-octagon",
                "title": "Services unavailable",
                "slug": "/",
            }
        ]

        return {"navbar_services": fallback}
