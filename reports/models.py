from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report {self.id} by {self.user.username}'


class Product(models.Model):
    sku = models.CharField(max_length=7, null=False, blank=False)
    product_name = models.CharField(max_length=255, null=False, blank=False)
    quantity_stock = models.IntegerField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sku} {self.product_name}'

    def save(self, *args, **kwargs):
        if not self.sku.startswith('0'):
            self.sku = self.sku.zfill(7)
        super(Product, self).save(*args, **kwargs)


class ReportProduct(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    quantity_found = models.IntegerField(null=False, blank=False)
    quantity_not_found = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Product Report {self.id} - Report {self.report.id}'
