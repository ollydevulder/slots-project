from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView

from .models import Shop


def index(request):
    return HttpResponse('This is the index page :)')

class ShopsView(ListView):
    model = Shop
    template_name = 'slots/shops.html'
    context_object_name = 'shop_list'

class ShopView(DetailView):
    model = Shop
    template_name = 'slots/shop-page.html'
    context_object_name = 'shop'
