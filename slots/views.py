from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

# Models

from .models import Shop
from django.contrib.auth.models import User

# Forms

from .forms import LoginForm, SignupForm

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
def login_view(request):  # slots:login
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
                return render(
                    request,
                    'slots/success.html',
                    {'message': 'You have been logged in.'}
                )
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
def logout_view(request):  # slots:logout
    logout(request)
    return redirect('slots:login')


@check_logged_in('slots:index', True)
def signup_view(request):  # slots:signup
    context = {
        'error_msg': [],
    }
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Form data is valid
            # Validate the clean data.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['check_password']

            # Is username taken?
            try:
                User.objects.get(username=username)
                # Yes
                context['error_msg'].append('Username taken.')
            except:
                pass

            # Is password valid?
            try:
                validate_password(password)
                # Yes
            except ValidationError as v:
                context['error_msg'].extend(v)

            # Do the passwords match?
            if password != password2:
                context['error_msg'].append('Passwords must match.')

            if len(context['error_msg']) == 0:
                # No errors
                # Create new user.
                user = User.objects.create_user(username, password=password)
                # Log user in.
                login(request, user)
                # Display success page.
                return render(
                    request, 
                    'slots/success.html', 
                    {'message': 'Your account has been created.'}
                )
        else:
            # Form data is invalid
            context['error_msg'] = 'Invalid form data.'

    form = SignupForm()
    context['form'] = form
    context['error'] = bool(len(context['error_msg']))

    return render(request, 'slots/signup.html', context)


@check_logged_in('slots:login')  # slots:index
def index(request):
    # Temporary redirect
    return redirect('slots:shops')


@method_decorator(check_logged_in('slots:login'), name='dispatch')
class ShopsView(ListView):  # slots:shops
    model = Shop
    template_name = 'slots/shops.html'
    context_object_name = 'shop_list'
    ordering = ['name']


@method_decorator(check_logged_in('slots:login'), name='dispatch')
class ShopView(DetailView):  # slots:view-shop
    model = Shop
    template_name = 'slots/shop-page.html'
    context_object_name = 'shop'
