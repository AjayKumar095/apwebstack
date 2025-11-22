from django.contrib import admin
from .models import *

# Register your models here.
class WhyChooseUsRowInline(admin.TabularInline):
    model = WhyChooseUsRow
    extra = 1
    fields = (
        "icon", "icon_color",
        "heading", "paragraph",
        "image", "image_alt"
    )

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("Heading", "Description")
    
@admin.register(TechnologyLogo)
class TechnologyLogoAdmin(admin.ModelAdmin):
    list_display = ("img_alt")   
    
@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("service",)
    inlines = [WhyChooseUsRowInline]