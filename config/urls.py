"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from reports import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('products/', views.product_view, name='product_view'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<pk>', views.product_update, name='product_update'),
    path('products/delete/<pk>', views.product_delete, name='product_delete'),
    path('product_reports/', views.product_report_view, name='product_report_view'),
    path('product_reports/create/', views.product_report_create, name='product_report_create'),
    path('product_reports/udpate/<pk>', views.product_report_update, name='product_report_update'),
    path('product_reports/delete/<pk>', views.product_report_delete, name='product_report_delete'),
    path('reports/create/', views.create_report, name='create_report'),
    path('reports/view/', views.report_view, name='report_view'),
    path('reports/detail/<int:report_id>/', views.report_detail, name='report_detail'),
    path('product_reports/detail/<int:product_report_id>/', views.product_report_detail, name='product_report_detail'),
]
