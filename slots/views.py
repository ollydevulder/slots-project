from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, ListView

from .models import Shop


def index(request):
    # Temporary redirect until user system added
    return redirect('/shops')


class ShopsView(ListView):
    model = Shop
    template_name = 'slots/shops.html'
    context_object_name = 'shop_list'
    ordering = ['name']


class ShopView(DetailView):
    model = Shop
    template_name = 'slots/shop-page.html'
    context_object_name = 'shop'
