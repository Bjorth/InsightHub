from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ReportForm, ProductForm, ProductReportForm
from .models import Product, ReportProduct
# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect('index')
    else:
        form = ReportForm()

    return render(request, 'reports/create_report.html', {'from': form})


@login_required
def product_view(request):
    products = Product.objects.all()
    return render(request, 'reports/product_view.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_view')
    else:
        form = ProductForm()
    return render(request, 'reports/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_view')
    else:
        form = ProductForm(instance=product)
    return render(request, 'reports/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_view')
    return render(request, 'reports/product_delete_approve.html', {'product': product})

@login_required
def product_report_view(request):
    reports = ReportProduct.objects.all()
    return render(request, 'reports/product_report_view.html', {'reports': reports})

@login_required
def product_report_create(request):
    if request.method == 'POST':
        form = ProductReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_report_view')
    else:
        form = ProductReportForm()
    return render(request, 'reports/product_report_form.html', {'form': form})

@login_required
def product_report_update(request, pk):
    report = get_object_or_404(ReportProduct, pk=pk)
    if request.method == 'POST':
        form = ProductReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('product_report_view')
    else:
        form = ProductReportForm(instance=report)
    return render(request, 'reports/product_report_form.html', {'form': form})

def product_report_delete(request, pk):
    report = get_object_or_404(ReportProduct, pk=pk)
    if request.method == 'POST':
        report.delete()
        return redirect('product_report_view')
    return render(request, 'reports/product_report_delete_approve.html', {'report': report})