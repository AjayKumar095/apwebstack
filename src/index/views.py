from django.shortcuts import render
from django.core.cache import cache
from src.logger import log_error, log_info

from .models import Hero_SectionIndex, WhyChooseUs_Index, Tech_LogoIndex, Index_Meta
from services.models import Add_Service

from .signals import INDEX_CACHE_KEY


def index(request):
    log_info("Rendering Index Page")

    try:
        # -------------------------------------------------
        # 1️⃣ Try to get cached index page data
        # -------------------------------------------------
        cached_data = cache.get(INDEX_CACHE_KEY)
        if cached_data is not None:
            log_info("Data Source: Cache")
            log_info(f"{cached_data}")
            return render(request, "index/index.html", {"index": cached_data})

        # -------------------------------------------------
        # 2️⃣ Cache empty → Fetch fresh data from DB
        # -------------------------------------------------
        log_info("Data Source: Database (fresh load)")

        hero = Hero_SectionIndex.objects.select_related("image").first()

        why_choose = (
            WhyChooseUs_Index.objects
            .prefetch_related("whychooseus_rows_images", "rows__icon")
            .first()
        )

        logos = Tech_LogoIndex.objects.select_related("logo_img").all()

        services = (
            Add_Service.objects
            .select_related("icon")
            .only("title", "slug", "short_description", "icon__class_name")[:6]
        )

        meta = Index_Meta.objects.first()

        # -------------------------------------------------
        # 3️⃣ Serialize everything nicely
        # -------------------------------------------------

        data = {
            "hero": hero,
            "why_choose_us": why_choose,
            "tech_logos": logos,
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
                "meta_title": meta.meta_title if meta else "Sample Title",
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

        # -------------------------------------------------
        # 4️⃣ Store to cache for 10 minutes (600 sec)
        # -------------------------------------------------

        cache.set(INDEX_CACHE_KEY, data, timeout=600)
        log_info("Index data stored in cache for 10 minutes")
        log_info(f"{data}")
        # -------------------------------------------------
        # 5️⃣ Return the response
        # -------------------------------------------------

        return render(request, "index/index.html", {"index": data})

    except Exception as e:
        log_error(
            f"Error occurred while rendering index page.\n"
            f"Exception: {type(e).__name__}\n"
            f"Message: {e}"
        )

        context = {
            "status": 404,
            "error": "Page Not Found",
            "message": (
                "Sorry, the page you are looking for doesn’t exist "
                "or may have been moved."
            ),
            "page": "index",
        }

        return render(
            request=request,
            template_name="error/errors.html",
            context=context,
            status=404
        )
