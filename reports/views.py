from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from .forms import ReportForm, ProductForm, ProductReportForm, ProductReportEditForm
from .models import Product, ReportProduct, Report
from .utility import normalize_text

import os

# Main view below
def index_view(request):
    return render(request, 'core/index.html')


# Views to reports below
@login_required
def report_view(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'report/report_view.html', {'reports': reports})


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, 'report/report_detail.html', {'report': report})


@login_required
def report_edit(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_detail', report_id=report.id)
    else:
        form = ReportForm(instance=report)
    return render(request, 'report/report_edit.html', {'form': form, 'report': report})


@staff_member_required
@login_required
def report_delete(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        report.delete()
        return redirect('report_view')
    return render(request, 'report/report_delete_approve.html', {'report': report})


# Views to product reports below
@login_required
def product_report_view(request):
    reports = ReportProduct.objects.filter(report__user=request.user)

    return render(request, 'product_report/product_report_view.html', {'reports': reports})


@login_required
def product_report_create(request):
    if request.method == 'POST':
        form = ProductReportForm(request.POST)
        if form.is_valid():
            today = timezone.now().date()
            report = Report.objects.filter(user=request.user, added__date=today).first()
            if not report:
                report = Report.objects.create(user=request.user)

            product = form.cleaned_data['product']
            quantity_found = form.cleaned_data['quantity_found']

            product_report = ReportProduct(
                report=report,
                product=product,
                quantity_found=quantity_found,
            )
            product_report.save()

            return redirect('product_report_view')
    else:
        form = ProductReportForm()
    return render(request, 'product_report/product_report_form.html', {'form': form})


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
    return render(request, 'product_report/product_report_form.html', {'form': form})


@staff_member_required
@login_required
def product_report_delete(request, pk):
    report = get_object_or_404(ReportProduct, pk=pk)
    if request.method == 'POST':
        report.product.save()
        report.delete()
        return redirect('product_report_view')
    return render(request, 'product_report/product_report_delete_approve.html', {'report': report})


@login_required
def product_report_detail(request, product_report_id):
    product_report = get_object_or_404(ReportProduct, pk=product_report_id)
    product_report.quantity_not_found = product_report.product.quantity_stock - product_report.quantity_found
    return render(request, 'product_report/product_report_detail.html', {'product_report': product_report})


@login_required
def product_report_edit(request, product_report_id):
    report = get_object_or_404(ReportProduct, pk=product_report_id)
    if request.method == 'POST':
        form = ProductReportEditForm(request.POST, instance=report)
        if form.is_valid():
            products = form.cleaned_data['products']
            quantity_found = form.cleaned_data['quantity_found']

            ReportProduct.objects.filter(report=report.report).delete()

            for product in products:
                product_report = ReportProduct(
                    report=report.report,
                    product=product,
                    quantity_found=quantity_found,
                    quantity_not_found=product.quantity_stock - quantity_found
                )
                product_report.save()

            return redirect('product_report_view')
    else:
        form = ProductReportEditForm(instance=report)
    return render(request, 'product_report/product_report_edit.html', {'form': form, 'report': report})


# Views to products below
@login_required
def product_view(request):
    products = Product.objects.all()
    return render(request, 'product/product_view.html', {'products': products})


@staff_member_required
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_view')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})


@staff_member_required
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
    return render(request, 'product/product_form.html', {'form': form})


@staff_member_required
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_view')
    return render(request, 'product/product_delete_approve.html', {'product': product})


# View to generate pdf report below
@login_required
def generate_pdf_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    product_reports = ReportProduct.objects.filter(report=report)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report_id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    icon_path = 'reports/static/favicon-192x192.png'
    if os.path.exists(icon_path):
        img = ImageReader(icon_path)
        p.drawImage(img, 50, height - 50, width=50, height=50, mask='auto')

    p.setFont('Helvetica', 12)

    margin_left = 50
    margin_bottom = 50
    margin_top = 50

    y = height - margin_top

    p.drawString(margin_left, y - 50, f'Report Title: {normalize_text(report.title)}')
    p.drawString(margin_left, y - 70, f'User: {normalize_text(report.user.username)}')
    p.drawString(margin_left, y - 90, f"Date Added: {report.added.strftime('%d-%m-%Y')}")

    p.drawString(margin_left, y - 110, 'Product Reports:')
    p.line(margin_left, y - 115, margin_left + 250, y - 115)

    line_height = 18

    total_products_sum = 0

    for product_report in product_reports:
        product = product_report.product

        y -= line_height * 5

        if y < margin_bottom:
            p.showPage()
            p.setFont('Helvetica', 12)
            y = height - margin_top - line_height

        normalized_product_name = normalize_text(product.product_name)
        total_product_value = product_report.quantity_found * product.unit_price
        p.drawString(margin_left + 20, y - 50, f'Product: {normalized_product_name}')
        p.drawString(margin_left + 20, y - 70, f'Quantity Found: {product_report.quantity_found}')
        p.drawString(margin_left + 20, y - 90, f'Quantity Not Found: {product_report.quantity_not_found}')
        p.drawString(margin_left + 20, y - 110, f'Total Product Value: {total_product_value} PLN')
        p.line(margin_left, y - 115, margin_left + 310, y - 115)

        total_products_sum += total_product_value

    p.drawString(margin_left, margin_bottom, f'Total Products Value: {total_products_sum} PLN')
    p.save()

    return response