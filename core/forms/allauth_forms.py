from django import forms
from allauth.account.forms import LoginForm
from allauth.account.forms import PasswordField

class CoreLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CoreLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'] = PasswordField(label='Lösenord')



class CoreSignupForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CoreSignupForm, self).__init__(*args, **kwargs)
        self.fields['password'] = PasswordField(label='Lösenord')