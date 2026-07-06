from django import forms
from .models import *
from inventory.models import *
from django.forms import formset_factory

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'phone', 'address', 'email', 'gstn')

class SelectSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_deleted=False)
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control'}) 

    class Meta:
        model = PurchaseBill
        fields = ['supplier']

class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'}) 
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '1', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '1', 'required': 'true'}) 

    class Meta:
        model = PurchaseItem
        fields = ['stock', 'quantity', 'perprice']

PurchaseItemFormSet = formset_factory(PurchaseItemForm, extra=1)

class PurchaseDetailsForm(forms.ModelForm):
    class Meta:
        model = PurchaseBillDetails
        fields = ('eway', 'veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total')

class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern': '[a-zA-Z\s]{1, 50}', 'title': 'Enter a valid name', 'required': 'true'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Enter a valid 10 digit phone number', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern': '[A-Z0-9]{15}', 'title': 'Enter a valid 15 digit GSTIN', 'required': 'true'})

    class Meta:
        model = SaleBill
        fields = ['name', 'phone', 'address', 'email', 'gstin']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'textinput form-control', 'rows': '4'})
        }

class SaleItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'}) 
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'}) 

    class Meta:
        model = SaleItem
        fields = ['stock', 'quantity', 'perprice']

SaleItemFormSet = formset_factory(SaleItemForm, extra=1)

class SaleDetailsForm(forms.ModelForm):
    class Meta:
        model = SaleBillDetails
        fields = ['eway', 'veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total']