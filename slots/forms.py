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

class UserSettingsForm(forms.Form):
    new_username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'new username',
    }), 
    required=False, 
    initial='', 
    help_text='Change username.')

    #new_password = forms.CharField(widget=forms.PasswordInput(attrs={
    #    'placeholder': 'new password',
    #}), required=False, help_text='Change password.')

    #new_check_password = forms.CharField(widget=forms.PasswordInput(attrs={
    #    'placeholder': 'check password',
    #}), required=False, help_text='Confirm new password.')
