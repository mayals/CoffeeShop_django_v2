from django.contrib import admin
from .models import ContactUsModel

# admin.site.register(ContactUsModel)



class ContactUsModelAdmin(admin.ModelAdmin):
    fields = ["name", "email", "created_at"]
    list_display = ["name", "email", "created_at"]
    search_fields = ["email"]

admin.site.register(ContactUsModel,ContactUsModelAdmin)