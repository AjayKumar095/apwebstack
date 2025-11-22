from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import (
    HeroSectionIndex,
    WhyChooseUsIndex,
    WhyChooseUsRowIndex,
    TechnologyLogoIndex,
)
from services.models import Add_Service


# 🟢 Cache key used by your index view
INDEX_CACHE_KEY = "index_page_data"


def clear_index_cache(reason=""):
    """
    Clear index page cache whenever related models change.
    """
    cache.delete(INDEX_CACHE_KEY)
    print(f"[Cache Cleared] → {reason}")


# -------------------------------
#      HERO SECTION TRACKING
# -------------------------------
@receiver(post_save, sender=HeroSectionIndex)
def hero_saved(sender, instance, **kwargs):
    clear_index_cache("HeroSectionIndex modified")


@receiver(post_delete, sender=HeroSectionIndex)
def hero_deleted(sender, instance, **kwargs):
    clear_index_cache("HeroSectionIndex deleted")


# -------------------------------
#      TECHNOLOGY LOGO TRACK
# -------------------------------
@receiver(post_save, sender=TechnologyLogoIndex)
def tech_logo_saved(sender, instance, **kwargs):
    clear_index_cache("TechnologyLogoIndex modified")


@receiver(post_delete, sender=TechnologyLogoIndex)
def tech_logo_deleted(sender, instance, **kwargs):
    clear_index_cache("TechnologyLogoIndex deleted")


# -------------------------------
#      WHY CHOOSE US (SECTION)
# -------------------------------
@receiver(post_save, sender=WhyChooseUsIndex)
def why_choose_saved(sender, instance, **kwargs):
    clear_index_cache("WhyChooseUsIndex modified")


@receiver(post_delete, sender=WhyChooseUsIndex)
def why_choose_deleted(sender, instance, **kwargs):
    clear_index_cache("WhyChooseUsIndex deleted")


# -------------------------------
#      WHY CHOOSE US (ROWS)
# -------------------------------
@receiver(post_save, sender=WhyChooseUsRowIndex)
def why_choose_row_saved(sender, instance, **kwargs):
    clear_index_cache("WhyChooseUsRowIndex modified")


@receiver(post_delete, sender=WhyChooseUsRowIndex)
def why_choose_row_deleted(sender, instance, **kwargs):
    clear_index_cache("WhyChooseUsRowIndex deleted")


# -------------------------------
#      SERVICES LIST (HOME PAGE)
# -------------------------------
@receiver(post_save, sender=Add_Service)
def service_saved(sender, instance, **kwargs):
    clear_index_cache("Add_Service modified")


@receiver(post_delete, sender=Add_Service)
def service_deleted(sender, instance, **kwargs):
    clear_index_cache("Add_Service deleted")
