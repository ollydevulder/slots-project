from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, ListView

# Models

from .models import Shop, Slot
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


LOGIN = 'slots:login'


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


@check_logged_in(LOGIN)
def logout_view(request):  # slots:logout
    logout(request)
    return redirect(LOGIN)


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


def index_view(request):  # slots:index
    context = {
        'users': User.objects.count(),
        'shops': Shop.objects.count(),
        'slots': Slot.objects.count(),
    }
    return render(request, 'slots/index.html', context=context)


@check_logged_in(LOGIN)
def user_view(request):  # slots:user
    return render(request, 'slots/user.html')


@check_logged_in(LOGIN)
def slot_manage_view(request, **kwargs):  # slots:manage-slot
    """
    The big daddy for slot views.
    """
    allowed_methods = {
        'book': book_slot_view,
        'cancel': cancel_slot_view,
        'modify': modify_slot_view,
    }

    try:
        # Do the shop and slot exist?
        shop = Shop.objects.get(pk=kwargs['shop'])
        slot = Slot.objects.get(shop=shop, position=kwargs['slot'])
        kwargs['shop'] = shop
        kwargs['slot'] = slot

        # Is the slot taken?
        taken = bool(slot.user)
        kwargs['taken'] = taken

        # Does the current user own the slot?
        owns = request.user == slot.user
        kwargs['owns'] = owns

        # Does the current user own any slots in the shop?
        owns_any = shop.slot_set.filter(user=request.user)
        kwargs['owns_any'] = bool(owns_any)
        if owns_any:
            kwargs['user_slot'] = owns_any[0]

        # Carry out the action.
        return allowed_methods[kwargs['method']](request, **kwargs)

    except:
        # Something went wrong.
        return redirect('slots:shops')


def book_slot_view(request, **kwargs):  # slots:manage-slot
    # If slot is free and current user does not own any slots from the shop...
    if not kwargs['taken'] and not kwargs['owns_any']:
        # Set the slot's owner to current user.
        slot = kwargs['slot']
        slot.user = request.user
        slot.save()

        # Render success page.
        shop = kwargs['shop']
        
        message = """You have booked slot #{} from <a href="{}">{}</a>.<br>
        You can view your booked slots <a href="{}">here</a>.
        """.format(
            slot.position + 1,
            reverse('slots:view-shop', args=[shop.pk]),
            shop.name,
            reverse('slots:slots')
        )
        context = {
            'message': message,
        }

        return render(request, 'slots/success.html', context=context)
    else:
        raise Exception('User not allowed to book this slot.')


def cancel_slot_view(request, **kwargs):  # slots:manage-slot
    # If slot is owned by current user...
    if kwargs['owns']:
        # Set the slot user to NULL.
        slot = kwargs['slot']
        slot.user = None
        slot.save()

        # Render success page.
        message = f'You have cancelled the slot.'
        context = {
            'message': message,
        }

        return render(request, 'slots/success.html', context=context)
    else:
        raise Exception('User can only cancel slots owned by them.')


def modify_slot_view(request, **kwargs): # slots:manage-slot
    # Does the user own a slot in this shop? (yes)
    # Is the slot taken? (no)
    if kwargs['owns_any'] and not kwargs['taken']:
        # Conditions satisfied.
        # Set the user's first slot's user to NULL.
        slot = kwargs['user_slot']
        slot.user = None
        slot.save()
        
        # Set new slot's user to user.
        slot = kwargs['slot']
        slot.user = request.user
        slot.save()

        # Render success page.
        shop = kwargs['shop']
        message = """You have modified your slot at <a href="{}">{}</a> from 
        #{} to #{}.<br>If you want to change it again go <a href="{}">here</a>.
        """.format(
            reverse('slots:view-shop', args=[shop.pk]),
            shop.name,
            kwargs['user_slot'].position + 1,
            slot.position + 1,
            reverse('slots:modify', args=[shop.pk])
        )
        context = {
            'message': message,
        }

        return render(request, 'slots/success.html', context=context)
    else:
        raise Exception('User cannot modify this slot.')


@check_logged_in(LOGIN)
def modify_view(request, **kwargs):  # slots:modify
    shop = Shop.objects.get(pk=kwargs['shop'])
    # Does the user have a slot in this shop?
    if shop.slot_set.filter(user=request.user):
        context = {
            'modify': True,
            'shop': shop,
        }
        return render(request, 'slots/shop-slots.html', context=context)
    else:
        return redirect('slots:shops')


@method_decorator(check_logged_in(LOGIN), name='dispatch')
class ShopsView(ListView):  # slots:shops
    model = Shop
    template_name = 'slots/shops.html'
    context_object_name = 'shop_list'
    ordering = ['name']


@method_decorator(check_logged_in(LOGIN), name='dispatch')
class ShopView(DetailView):  # slots:view-shop
    model = Shop
    template_name = 'slots/shop-slots.html'
    context_object_name = 'shop'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add 'owns' var for template styling.
        # Does the shop have a slot owned by the current user?
        context['owns'] = bool(
            context['shop'].slot_set.filter(user=self.request.user)
        )

        context['modify'] = False

        return context




@method_decorator(check_logged_in(LOGIN), name='dispatch')
class SlotsView(ListView):  # slots:slots
    def get_queryset(self):
        return self.request.user.slot_set.all()

    template_name = 'slots/slots.html'
    context_object_name = 'slots'
