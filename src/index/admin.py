from django.contrib import admin
from .models import *

# Register your models here.
class WhyChooseUsRowInline(admin.TabularInline):
    model = WhyChooseUsRowIndex
    extra = 1
    fields = (
        "icon", "icon_color",
        "heading", "paragraph",
        "image", "image_alt"
    )
    
@admin.register(IndexMeta)
class IndexMetaAdmin(admin.ModelAdmin):
    list_display = ("meta_title", "meta_description", "meta_keywords")      

@admin.register(HeroSectionIndex)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("Heading", "Description")
    
@admin.register(TechnologyLogoIndex)
class TechnologyLogoAdmin(admin.ModelAdmin):
    list_display = ("logo_alt",)   
    
@admin.register(WhyChooseUsIndex)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("Heading",)
    inlines = [WhyChooseUsRowInline]