from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

# Models

from .models import Shop

# Forms

from .forms import LoginForm

# Decorators

from django.utils.decorators import method_decorator

def logged_in(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('slots:login')
    return wrapper

def not_logged_in(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('slots:index')
    return wrapper

# Views

@not_logged_in
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Valid form data in form.cleaned_data
            # Attempt to authenticate.
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                # Login the session.
                login(request, user)
                # Render success page.
                return render(request, 'slots/success.html')
            else:
                # Not authenticated
                context['error_msg'] = 'Login details incorrect.'
        else:
            # Invalid form data
            context['error_msg'] = 'Invalid form data.'

    form = LoginForm()
    context['form'] = form
    context['error'] = 'error_msg' in context

    return render(
        request,
        'slots/login.html',
        context,
    )


@logged_in
def logout_view(request):
    logout(request)
    return redirect('slots:login')


@logged_in
def index(request):
    # Temporary redirect
    return redirect('slots:shops')


@method_decorator(logged_in, name='dispatch')
class ShopsView(ListView):
    model = Shop
    template_name = 'slots/shops.html'
    context_object_name = 'shop_list'
    ordering = ['name']


@method_decorator(logged_in, name='dispatch')
class ShopView(DetailView):
    model = Shop
    template_name = 'slots/shop-page.html'
    context_object_name = 'shop'
