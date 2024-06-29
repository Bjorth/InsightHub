from django import forms

from .models import Report, ReportProduct, Product


# Form for Report below
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title',)


# Form for Product below
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'product_name', 'quantity_stock', 'unit_price']

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        if not sku.startswith('0'):
            sku = sku.zfill(7)
        return sku


# Form for Product Reports below
class ProductReportForm(forms.ModelForm):
    class Meta:
        model = ReportProduct
        fields = ['product', 'quantity_found']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProductReportEditForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = ReportProduct
        fields = ['products', 'quantity_found']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['products'].initial = [self.instance.product]
