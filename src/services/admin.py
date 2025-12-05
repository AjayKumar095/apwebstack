from django.contrib import admin
from .models import *


@admin.register(Service_Meta)
class ServiceMetaAdmin(admin.ModelAdmin):
    list_display = ("meta_title", "meta_description", "meta_keywords")   

@admin.register(Add_Service)
class AddServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "slug", "data_created")
    search_fields = ("title", "icon")   # <-- Search bar added here
    autocomplete_fields = ('icon',)
    
class ServiceDetailBulletInline(admin.TabularInline):
    model = Service_DetailBullet
    extra = 1
    can_delete = True


class ServiceBenefitRowInline(admin.TabularInline):
    model = Service_BenefitRow
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


@admin.register(Service_Hero)
class Service_HeroAdmin(admin.ModelAdmin):
    list_display = ("service", "heading")


@admin.register(Service_Details)
class Service_DetailsAdmin(admin.ModelAdmin):
    list_display = ("service", "heading")
    inlines = [ServiceDetailBulletInline]



@admin.register(Service_Benefits)
class Service_BenefitsAdmin(admin.ModelAdmin):
    list_display = ("service", "heading")
    inlines = [ServiceBenefitRowInline]
 


@admin.register(WhyChoose_Us)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("service",)
    inlines = [WhyChooseUsRowInline]
  
