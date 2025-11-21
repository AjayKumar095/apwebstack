from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import (
    Add_Service,
    ServiceHero,
    ServiceDetails,
    ServiceBenefits,
    WhyChooseUs,
    ServiceDetailBullet,
    ServiceBenefitRow,
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
@receiver([post_save, post_delete], sender=ServiceHero)
def clear_hero_cache(sender, instance, **kwargs):
    clear_cache(instance.service.slug)


# ---- DETAILS ----
@receiver([post_save, post_delete], sender=ServiceDetails)
def clear_details_cache(sender, instance, **kwargs):
    clear_cache(instance.service.slug)


@receiver([post_save, post_delete], sender=ServiceDetailBullet)
def clear_detail_bullet_cache(sender, instance, **kwargs):
    clear_cache(instance.section.service.slug)


# ---- BENEFITS ----
@receiver([post_save, post_delete], sender=ServiceBenefits)
def clear_benefits_cache(sender, instance, **kwargs):
    clear_cache(instance.service.slug)


@receiver([post_save, post_delete], sender=ServiceBenefitRow)
def clear_benefit_row_cache(sender, instance, **kwargs):
    clear_cache(instance.section.service.slug)


# ---- WHY CHOOSE ----
@receiver([post_save, post_delete], sender=WhyChooseUs)
def clear_why_choose_cache(sender, instance, **kwargs):
    clear_cache(instance.service.slug)


@receiver([post_save, post_delete], sender=WhyChooseUsRow)
def clear_why_choose_row_cache(sender, instance, **kwargs):
    clear_cache(instance.section.service.slug)
