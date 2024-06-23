from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import RegisterForm, ReportForm, ProductForm, ProductReportForm
from .models import Product, ReportProduct, Report


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
            today = timezone.now().date()
            existing_report = Report.objects.filter(user=request.user, added__date=today).first()
            if not existing_report:
                report = form.save(commit=False)
                report.user = request.user
                report.save()
                return redirect('index')
    else:
        form = ReportForm()
    return render(request, 'reports/create_report.html', {'from': form})


@login_required
def report_view(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'reports/report_view.html', {'reports': reports})


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    product_reports = ReportProduct.objects.filter(report=report)
    return render(request, 'report/report_detail.html',
                  {'report': report, 'product_reports': product_reports})


@login_required
def product_report_detail(request, product_report_id):
    product_report = get_object_or_404(ReportProduct, pk=product_report_id)
    product_report.quantity_not_found = product_report.product.quantity_stock - product_report.quantity_found
    return render(request, 'report/product_report_detail.html', {'product_report': product_report})


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

    for report in reports:
        report.quantity_not_found = report.product.quantity_stock - report.quantity_found

    return render(request, 'reports/product_report_view.html', {'reports': reports})


@login_required
def product_report_create(request):
    if request.method == 'POST':
        form = ProductReportForm(request.POST)
        if form.is_valid():
            today = timezone.now().date()
            report = Report.objects.filter(user=request.user, added__date=today).first()
            if not report:
                report = Report.objects.create(user=request.user)

            product_report = form.save(commit=False)
            product_report.report = report

            product_stock = product_report.product.quantity_stock
            product_report.quantity_not_found = product_stock - product_report.quantity_found

            product_report.save()

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
            updated_report = form.save(commit=False)

            difference = updated_report.quantity_found - report.quantity_found
            report.product.quantity_stock -= difference
            report.product.save()

            updated_report.save()
            return redirect('product_report_view')
    else:
        form = ProductReportForm(instance=report)
    return render(request, 'reports/product_report_form.html', {'form': form})


@login_required
def product_report_delete(request, pk):
    report = get_object_or_404(ReportProduct, pk=pk)
    if request.method == 'POST':
        report.product.save()
        report.delete()
        return redirect('product_report_view')
    return render(request, 'reports/product_report_delete_approve.html', {'report': report})
