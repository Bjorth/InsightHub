from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Report, ReportProduct, Product


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Please enter a valid email address')

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2')


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'user' in self.fields:
            del self.fields['user']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'product_name', 'quantity_stock', 'unit_price']

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        if not sku.startswith('0'):
            sku = sku.zfill(7)
        return sku


class ProductReportForm(forms.ModelForm):
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
        self.fields.pop('product')
