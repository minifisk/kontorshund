from django import forms
from allauth.account.forms import LoginForm
from allauth.account.forms import PasswordField

class CoreLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CoreLoginForm, self).__init__(*args, **kwargs)
        ## here i add the new fields that i need
        self.fields['password'] = PasswordField(label='Lösenord')
