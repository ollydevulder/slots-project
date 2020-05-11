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

class check_logged_in(object):
    """
    For wrapping view functions.\n
    Checks if the user is authenticated and 
    redirects based on this and the `invert` argument.
    """
    def __init__(self, redirect_view, invert=False):
        self.redirect_view = redirect_view
        self.invert = bool(invert)
        
    def __call__(self, func):
        def wrapper(request, *args, **kwargs):
            if bool(request.user.is_authenticated) ^ self.invert:
                return func(request, *args, **kwargs)
            else:
                return redirect(self.redirect_view)
        return wrapper

# Views

@check_logged_in('slots:shops', True)
def login_view(request): # slots:login
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


@check_logged_in('slots:login')
def logout_view(request): # slots:logout
    logout(request)
    return redirect('slots:login')


@check_logged_in('slots:login') # slots:index
def index(request):
    # Temporary redirect
    return redirect('slots:shops')


@method_decorator(check_logged_in('slots:login'), name='dispatch')
class ShopsView(ListView): # slots:shops
    model = Shop
    template_name = 'slots/shops.html'
    context_object_name = 'shop_list'
    ordering = ['name']


@method_decorator(check_logged_in('slots:login'), name='dispatch')
class ShopView(DetailView): # slots:view-shop
    model = Shop
    template_name = 'slots/shop-page.html'
    context_object_name = 'shop'
