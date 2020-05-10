from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from .models import Shop


def check_user(func):
    """
    User authentication decorator\n
    Redirects to login page if User not authenticated.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('slots:login')
    return wrapper


def login_view(request):
    template_name = 'slots/login.html'
    failed = False

    if request.user.is_authenticated:
        # If already logged in then redirect.
        return redirect('/')

    if request.method == 'POST':
        if not set(['username', 'password']).issubset(set(request.POST)):
            # Form does not have required values
            failed = True
        else:
            # Get form values.
            username = request.POST['username']
            password = request.POST['password']

            # Attempt login.
            user = authenticate(username=username, password=password)
            if user is not None:
                # Login success
                login(request, user)
                # Render success page.
                return render(request, 'slots/success.html')
            else:
                # Login failed
                failed = True

    return render(
        request, 
        template_name=template_name, 
        context={ 'failed': failed },
    )

@check_user
def logout_view(request):
    logout(request)
    return redirect('slots:login')

@check_user
def index(request):
    # Temporary redirect
    return redirect('slots:shops')


@method_decorator(check_user, name='dispatch')
class ShopsView(ListView):
    model = Shop
    template_name = 'slots/shops.html'
    context_object_name = 'shop_list'
    ordering = ['name']


@method_decorator(check_user, name='dispatch')
class ShopView(DetailView):
    model = Shop
    template_name = 'slots/shop-page.html'
    context_object_name = 'shop'
