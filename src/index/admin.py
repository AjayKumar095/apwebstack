from django.contrib import admin
from .models import *

# Register your models here.
class WhyChooseUsRowInline(admin.TabularInline):
    model = WhyChooseUsRow_Index
    extra = 1
    fields = (
        "icon", "icon_color",
        "heading", "paragraph",
        "image", "image_alt"
    )
    
@admin.register(Index_Meta)
class Index_MetaAdmin(admin.ModelAdmin):
    list_display = ("meta_title", "meta_description", "meta_keywords")      

@admin.register(Hero_SectionIndex)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("Heading", "Description", "image")
    
@admin.register(Tech_LogoIndex)
class TechnologyLogoAdmin(admin.ModelAdmin):
    list_display = ("logo_alt",)   
    
@admin.register(WhyChooseUs_Index)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("Heading",)
    inlines = [WhyChooseUsRowInline]