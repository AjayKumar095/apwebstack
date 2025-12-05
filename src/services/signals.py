from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import (
    Add_Service,
    Service_Hero,
    Service_Details,
    Service_Benefits,
    WhyChoose_Us,
    Service_DetailBullet,
    Service_BenefitRow,
    WhyChooseUsRow
)


def clear_cache(slug):
    cache_key = f"service_detail_{slug}"
    cache.delete(cache_key)


# ---- MAIN SERVICE ----
@receiver([post_save, post_delete], sender=Add_Service)
def clear_add_service_cache(sender, instance, **kwargs):
    clear_cache(instance.slug)


# ---- HERO ----
@receiver([post_save, post_delete], sender=Service_Hero)
def clear_hero_cache(sender, instance, **kwargs):
    clear_cache(instance.service.slug)


# ---- DETAILS ----
@receiver([post_save, post_delete], sender=Service_Details)
def clear_details_cache(sender, instance, **kwargs):
    clear_cache(instance.service.slug)


@receiver([post_save, post_delete], sender=Service_DetailBullet)
def clear_detail_bullet_cache(sender, instance, **kwargs):
    clear_cache(instance.section.service.slug)


# ---- BENEFITS ----
@receiver([post_save, post_delete], sender=Service_Benefits)
def clear_benefits_cache(sender, instance, **kwargs):
    clear_cache(instance.service.slug)


@receiver([post_save, post_delete], sender=Service_BenefitRow)
def clear_benefit_row_cache(sender, instance, **kwargs):
    clear_cache(instance.section.service.slug)


# ---- WHY CHOOSE ----
@receiver([post_save, post_delete], sender=WhyChoose_Us)
def clear_why_choose_cache(sender, instance, **kwargs):
    clear_cache(instance.service.slug)


@receiver([post_save, post_delete], sender=WhyChooseUsRow)
def clear_why_choose_row_cache(sender, instance, **kwargs):
    clear_cache(instance.section.service.slug)
