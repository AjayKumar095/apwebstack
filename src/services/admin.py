from django.contrib import admin
from .models import *

@admin.register(Add_Service)
class AddServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "slug", "data_created")
    search_fields = ("title", "icon")   # <-- Search bar added here
    autocomplete_fields = ('icon',)
    
admin.site.register(ServiceHero)
admin.site.register(ServiceDetails)
admin.site.register(ServiceBenefits)
admin.site.register(WhyChooseUs)