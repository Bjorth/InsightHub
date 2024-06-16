from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report {self.id} by {self.user.username}'

class Product(models.Model):
    sku = models.IntegerField()
    product_name = models.CharField(max_length=255)
    quantity_stock = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Product {self.product_name}'

class ReportProduct(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_found = models.IntegerField()

    def __str__(self):
        return f'ReportProduct {self.id} - Report {self.report.id} - Product {self.product.id}'