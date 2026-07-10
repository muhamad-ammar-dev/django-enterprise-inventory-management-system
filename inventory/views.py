from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .filters import *
from .forms import *
from django_filters.views import FilterView
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
# Create your views here.

class StockListView(FilterView):
    queryset = Stock.objects.filter(is_deleted=False)
    filterset_class = StockFilter
    template_name = 'inventory.html'
    context_object_name = 'stocks'
    paginate_by = 10

class CreateStock(SuccessMessageMixin, generic.CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'create_stock.html'
    success_url = '/'
    success_message = "Stock created successfully."

class UpdateStock(SuccessMessageMixin, generic.UpdateView):
    model = Stock
    form_class = StockForm
    template_name = 'update_stock.html'
    success_url = '/inventory/stock_list/'
    success_message = "Stock updated successfully."

class DeleteStock(generic.View):
    template_name = 'delete_stock.html'
    success_message = "Stock deleted successfully."
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'stock': stock})
    
    def post(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()
        messages.success(request, self.success_message)
        return redirect('stock_list')

