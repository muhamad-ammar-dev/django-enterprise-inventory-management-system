from django.urls import path
from .views import *

urlpatterns = [
    path('create_supplier/', CreateSupplier.as_view(), name='create_supplier'),
    path('supplier_list/', SupplierList.as_view(), name='supplier_list'),
    path('supplier/<str:name>/', SupplierView.as_view(), name='supplier'),
    path('update_supplier/<str:pk>/', UpdateSupplier.as_view(), name='update_supplier'),
    path('delete_supplier/<str:pk>/', DeleteSupplier.as_view(), name='delete_supplier'),
    # Purchase urls
    path('purchases/', PurchaseView.as_view(), name='purchases'),
    path('select_supplier/', SelectSupplierView.as_view(), name='select_supplier'),
    path('new_purchase/<str:pk>/', PurchaseCreateView.as_view(), name='new_purchase'),
    path('purchase_delete/<str:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    path('purchase_bill/<str:billno>/', PurchaseBillView.as_view(), name='purchase_bill'),




]