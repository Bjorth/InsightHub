import unicodedata

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from .forms import RegisterForm, ReportForm, ProductForm, ProductReportForm, ProductReportEditForm
from .models import Product, ReportProduct, Report


# Main view below
def index_view(request):
    return render(request, 'index.html')


# Registration view below:
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
    return render(request, 'registration/register.html', {'form': form})


# Views to reports below
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

    product_quantities_found = {}

    for report in reports:
        product_id = report.product.id
        if product_id in product_quantities_found:
            product_quantities_found[product_id] += report.quantity_found
        else:
            product_quantities_found[product_id] = report.quantity_found

    for report in reports:
        product_id = report.product.id
        product_stock = report.product.quantity_stock
        quantity_found = product_quantities_found.get(product_id, 0)
        report.quantity_not_found = product_stock - quantity_found
        report.save()

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
                quantity_not_found=product.quantity_stock - quantity_found
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


# View to generate pdf report below
@login_required
def generate_pdf_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    product_reports = ReportProduct.objects.filter(report=report)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report_id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont('Helvetica', 12)

    margin_left = 50
    margin_bottom = 50
    margin_top = 50

    y = height - margin_top

    def normalize_text(text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    p.drawString(margin_left, y, f'Report Title: {normalize_text(report.title)}')
    p.drawString(margin_left, y - 20, f'User: {normalize_text(report.user.username)}')
    p.drawString(margin_left, y - 40, f"Date Added: {report.added.strftime('%d-%m-%Y')}")

    p.drawString(margin_left, y - 60, 'Product Reports:')
    p.line(margin_left, y - 65, margin_left + 200, y - 65)

    line_height = 15

    for product_report in product_reports:
        product = product_report.product

        y -= line_height * 4

        if y < margin_bottom:
            p.showPage()
            p.setFont('Helvetica', 12)
            y = height - margin_top - line_height

        normalized_product_name = normalize_text(product.product_name)

        p.drawString(margin_left + 20, y - 40, f'Product: {normalized_product_name}')
        p.drawString(margin_left + 20, y - 60, f'Quantity Found: {product_report.quantity_found}')
        p.drawString(margin_left + 20, y - 80, f'Quantity Not Found: {product_report.quantity_not_found}')
        p.line(margin_left, y - 85, margin_left + 220, y - 85)

    p.save()

    return response
