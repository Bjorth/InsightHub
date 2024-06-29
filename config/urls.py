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

from reports import views as views_report
from account_managment import views as views_account

urlpatterns = [
    # Main path below
    path('', views_report.index_view, name='index'),
    # Admin and accounts paths below
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views_account.register_view, name='register'),
    # Product paths below
    path('products/', views_report.product_view, name='product_view'),
    path('products/create/', views_report.product_create, name='product_create'),
    path('products/update/<pk>', views_report.product_update, name='product_update'),
    path('products/delete/<pk>', views_report.product_delete, name='product_delete'),
    # Product reports paths below
    path('product_reports/', views_report.product_report_view, name='product_report_view'),
    path('product_reports/create/', views_report.product_report_create, name='product_report_create'),
    path('product_reports/udpate/<pk>', views_report.product_report_update, name='product_report_update'),
    path('product_reports/delete/<pk>', views_report.product_report_delete, name='product_report_delete'),
    path('product_reports/detail/<int:product_report_id>/', views_report.product_report_detail, name='product_report_detail'),
    path('product_reports/<int:product_report_id>/edit/', views_report.product_report_edit, name='product_report_edit'),
    # Reports path below
    path('reports/view/', views_report.report_view, name='report_view'),
    path('reports/detail/<int:report_id>/', views_report.report_detail, name='report_detail'),
    path('reports/<int:report_id>/edit/', views_report.report_edit, name='report_edit'),
    path('reports/<int:report_id>/delete/', views_report.report_delete, name='report_delete'),
    # Generate pdf report file path below
    path('reports/<int:report_id>/pdf/', views_report.generate_pdf_report, name='generate_pdf_report'),
]
