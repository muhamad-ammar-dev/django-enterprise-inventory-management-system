from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from transaction.models import SaleBill, PurchaseBill
from inventory.models import Stock


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    sales = SaleBill.objects.order_by('-time')[:3]
    purchases = PurchaseBill.objects.order_by('-time')[:3]

    stocks = Stock.objects.filter(is_deleted=False)

    labels = list(stocks.values_list('name', flat=True))
    data = [float(quantity) for quantity in stocks.values_list('quantity', flat=True)]

    context = {
        'sales': sales,
        'purchases': purchases,
        'labels': labels,
        'data': data,
    }

    return render(request, 'home.html', context)

class AboutView(TemplateView):
    template_name = "about.html"