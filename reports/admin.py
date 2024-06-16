from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Report, ReportProduct, Product

# Register your models here.
admin.site.register(Report)
admin.site.register(ReportProduct)
admin.site.register(Product)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
