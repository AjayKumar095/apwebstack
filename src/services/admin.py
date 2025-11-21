from django.contrib import admin
from .models import *

@admin.register(Add_Service)
class AddServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "slug", "data_created")
    search_fields = ("title", "icon")   # <-- Search bar added here
    autocomplete_fields = ('icon',)
    
class ServiceDetailBulletInline(admin.TabularInline):
    model = ServiceDetailBullet
    extra = 1


class ServiceBenefitRowInline(admin.TabularInline):
    model = ServiceBenefitRow
    extra = 1
    fields = (
        "icon", "icon_color",
        "heading", "paragraph",
        "image", "image_alt"
    )


class WhyChooseUsRowInline(admin.TabularInline):
    model = WhyChooseUsRow
    extra = 1
    fields = (
        "icon", "icon_color",
        "heading", "paragraph",
        "image", "image_alt"
    )


@admin.register(ServiceHero)
class ServiceHeroAdmin(admin.ModelAdmin):
    list_display = ("service", "heading")


@admin.register(ServiceDetails)
class ServiceDetailsAdmin(admin.ModelAdmin):
    list_display = ("service", "heading")
    inlines = [ServiceDetailBulletInline]



@admin.register(ServiceBenefits)
class ServiceBenefitsAdmin(admin.ModelAdmin):
    list_display = ("service", "heading")
    inlines = [ServiceBenefitRowInline]
 


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("service",)
    inlines = [WhyChooseUsRowInline]
  
