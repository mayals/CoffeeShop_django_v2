from django.contrib import admin
from .models import UserModel, UserProfile,SMSCode 

admin.site.register(UserModel)
admin.site.register(UserProfile)
admin.site.register(SMSCode)