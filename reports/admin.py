from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Report, ReportProduct, Product

# Registered models from models.py
admin.site.register(Report)
admin.site.register(ReportProduct)
admin.site.register(Product)

# Default settings from Django for registration and account management
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
