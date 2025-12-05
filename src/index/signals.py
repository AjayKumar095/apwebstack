from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import (
    Hero_SectionIndex,
    WhyChooseUs_Index,
    WhyChooseUsRow_Index,
    Tech_LogoIndex,
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
@receiver(post_save, sender=Hero_SectionIndex)
def hero_saved(sender, instance, **kwargs):
    clear_index_cache("Hero_SectionIndex modified")


@receiver(post_delete, sender=Hero_SectionIndex)
def hero_deleted(sender, instance, **kwargs):
    clear_index_cache("Hero_SectionIndex deleted")


# -------------------------------
#      TECHNOLOGY LOGO TRACK
# -------------------------------
@receiver(post_save, sender=Tech_LogoIndex)
def tech_logo_saved(sender, instance, **kwargs):
    clear_index_cache("Tech_LogoIndex modified")


@receiver(post_delete, sender=Tech_LogoIndex)
def tech_logo_deleted(sender, instance, **kwargs):
    clear_index_cache("Tech_LogoIndex deleted")


# -------------------------------
#      WHY CHOOSE US (SECTION)
# -------------------------------
@receiver(post_save, sender=WhyChooseUs_Index)
def why_choose_saved(sender, instance, **kwargs):
    clear_index_cache("WhyChooseUs_Index modified")


@receiver(post_delete, sender=WhyChooseUs_Index)
def why_choose_deleted(sender, instance, **kwargs):
    clear_index_cache("WhyChooseUs_Index deleted")


# -------------------------------
#      WHY CHOOSE US (ROWS)
# -------------------------------
@receiver(post_save, sender=WhyChooseUsRow_Index)
def why_choose_row_saved(sender, instance, **kwargs):
    clear_index_cache("WhyChooseUsRow_Index modified")


@receiver(post_delete, sender=WhyChooseUsRow_Index)
def why_choose_row_deleted(sender, instance, **kwargs):
    clear_index_cache("WhyChooseUsRow_Index deleted")


# -------------------------------
#      SERVICES LIST (HOME PAGE)
# -------------------------------
@receiver(post_save, sender=Add_Service)
def service_saved(sender, instance, **kwargs):
    clear_index_cache("Add_Service modified")


@receiver(post_delete, sender=Add_Service)
def service_deleted(sender, instance, **kwargs):
    clear_index_cache("Add_Service deleted")
