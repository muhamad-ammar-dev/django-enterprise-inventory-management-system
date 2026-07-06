from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
# Create your views here.

class CreateSupplier(SuccessMessageMixin, generic.CreateView):
    model = Supplier
    form_class = SupplierForm
    success_message = "Supplier created successfully."
    success_url = '/inventory/supplier_list/'
    template_name = 'supplier/create_supplier.html'
    
class SupplierList(generic.ListView):
    model = Supplier
    queryset = Supplier.objects.filter(is_deleted=False)
    template_name = 'supplier/suppliers_list.html'
    context_object_name = 'supplier'
    paginate_by = 1

class UpdateSupplier(SuccessMessageMixin, generic.UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_message = "Supplier updated successfully."
    success_url = '/transaction/supplier_list'
    template_name = 'supplier/update_supplier.html' 

class DeleteSupplier(generic.View):
    template_name = 'supplier/delete_supplier.html'
    success_message = "Supplier deleted successfully."
    
    def get(self, request, pk):
        sup = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'sup': sup})
    
    def post(self, request, pk):
        sup = get_object_or_404(Supplier, pk=pk)
        sup.is_deleted = True
        sup.save()
        messages.success(request, self.success_message)
        return redirect('supplier_list')

class SupplierView(generic.View):
    def get(self, request, name):
        supobjc = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supobjc)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 1)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier': supobjc,
            'bills': bills
        }
        return render(request, 'supplier/supplier.html', context)


class PurchaseView(generic.ListView):
    model = PurchaseBill
    template_name = 'purchase/purchases_list.html'
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 1

class SelectSupplierView(generic.View):
    form_class = SelectSupplierForm
    template_name = 'purchase/select_supplier.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get('supplier')
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new_purchase', supplier.id)
        return render(request, self.template_name, {'form': form})
    
class PurchaseCreateView(generic.View):
    template_name = 'purchase/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormSet(request.GET or None)
        supplierobj = get_object_or_404(Supplier, pk=pk)
        context = {
            'formset': formset,
            'supplier': supplierobj,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        formset = PurchaseItemFormSet(request.POST)
        supplierobj = get_object_or_404(Supplier, pk=pk)
        if formset.is_valid():
            # Save bill
            billobj = PurchaseBill(supplier=supplierobj)
            billobj.save()
            # Save bill details
            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:
                billitem = form.save(commit=False)
                billitem.billno = billobj
                stock = get_object_or_404(Stock, name=billitem.stock.name)
                billitem.totalprice = billitem.quantity * billitem.perprice
                stock.quantity += billitem.quantity
                stock.save()
                billitem.save()
            messages.success(request, "Purchase items added successfully.")
            return redirect('purchase_bill', billno=billobj.billno)
            # return redirect('/')
        formset = PurchaseItemFormSet(request.GET or None)
        context = {
            'formset': formset,
            'supplier': supplierobj,
        }
        return render(request, self.template_name, context)

# class PurchaseDeleteView(SuccessMessageMixin, generic.DetailView):
#     model = PurchaseBill
#     template_name = 'purchase/delete_purchase.html'
#     success_url = '/transaction/purchases'

#     def post(self, *args, **kwargs):
#         self.object = self.get_object()
#         items = PurchaseBill.objects.filter(billno=self.object.billno)
#         for item in items:
#             stock = get_object_or_404(Stock, name=item.stock.name)
#             if stock.is_deleted == False:
#                 stock.quantity -= item.quantity
#                 stock.save()
#         messages.success(self.request, "Purchase bill deleted successfully.")
#         return super(PurchaseDeleteView, self).delete(*args, **kwargs)

class PurchaseDeleteView(generic.View):
    template_name = 'purchase/delete_purchase.html'
    def get(self, request, pk):
        bill = get_object_or_404(PurchaseBill, pk=pk)
        return render(request, self.template_name, {"object": bill})
    def post(self, request, pk):
        bill = get_object_or_404(PurchaseBill, pk=pk)
        items = PurchaseItem.objects.filter(billno=bill)
        for item in items:
            stock = get_object_or_404(Stock, pk=item.stock.pk)
            if not stock.is_deleted:
                stock.quantity -= item.quantity
                stock.save()
        bill.delete()
        messages.success(request, "Purchase bill deleted successfully.")
        return redirect("purchases")
    
class PurchaseBillView(generic.View):
    model = PurchaseBill
    template_name = 'bill/purchase_bill.html'
    bill_base = 'bill/bill_base.html'
    form_class = PurchaseDetailsForm

    def get_bill_context(self, billno, form):
        bill = get_object_or_404(PurchaseBill, billno=billno)
        items = PurchaseItem.objects.filter(billno=billno)
        billdetails = get_object_or_404(PurchaseBillDetails, billno=billno)
        return {
            'bill': bill,
            'items': items,
            'billdetails': billdetails,
            'bill_base': self.bill_base,
            'form': form,
        }
        
    def get(self, request, billno):
        billdetalisobj = get_object_or_404(PurchaseBillDetails, billno=billno)
        form = self.form_class(instance=billdetalisobj)
        context = self.get_bill_context(billno, form)
        return render(request, self.template_name, context)
    
    def post(self, request, billno):
        billdetalisobj = get_object_or_404(PurchaseBillDetails, billno=billno)
        form = self.form_class(request.POST, instance=billdetalisobj)
        if form.is_valid():
            form.save()
            messages.success(request, "Purchase bill details updated successfully.")
        else:
            messages.error(request, "Error updating purchase bill details.")
        context = self.get_bill_context(billno, form)
        return render(request, self.template_name, context)
    
class SaleCreateView(generic.View):
    template_name = 'sales/create_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormSet(request.GET or None)
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            billobj = form.save(commit=False)
            billobj.save()

            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()

            for form in formset:
                billitem = form.save(commit=False)
                billitem.billno = billobj
                stock = get_object_or_404(Stock, name=billitem.stock.name)
                billitem.totalprice = billitem.perprice * billitem.quantity
                stock.quantity -= billitem.quantity
                stock.save()
                billitem.save()
            messages.success(request, "Purchase bill has been created successfully.")
            return redirect('sale-bill', billno = billobj.billno)
        form = SaleForm(request.GET or None)
        formset = SaleItemFormSet(request.GET or None)
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, self.template_name, context)

    
    