from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password',
    }))


class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'username',
    }))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={
    #     'placeholder': 'email',
    # }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password',
    }))
    check_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'check password',
    }))