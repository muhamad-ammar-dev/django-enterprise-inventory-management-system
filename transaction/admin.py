from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([Supplier, PurchaseBill, PurchaseItem, PurchaseBillDetails, SaleBill, SaleItem, SaleBillDetails])
