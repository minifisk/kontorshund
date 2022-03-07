from django import forms
from allauth.account.forms import LoginForm, SignupForm
from allauth.account.forms import PasswordField

class CoreLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CoreLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'] = PasswordField(label='Lösenord')



class CoreSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CoreSignupForm, self).__init__(*args, **kwargs)
        self.fields['password'] = PasswordField(label='Lösenord')

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CoreSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user