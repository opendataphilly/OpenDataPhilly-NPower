from django import forms

from registration.backends.default import DefaultBackend
from registration.forms import RegistrationForm,RegistrationFormUniqueEmail
from django.db import transaction

class ODPRegistrationForm(RegistrationForm):
      
    first_name = forms.RegexField(regex=r'^\w',
                                max_length=30,
                                widget=forms.TextInput(),
                                label="First Name",
                                error_messages={ 'invalid': "This value must contain only letters" },
                                required=True)
    last_name = forms.RegexField(regex=r'^\w',
                                max_length=30,
                                widget=forms.TextInput(),
                                label="Last Name",
                                error_messages={ 'invalid': "This value must contain only letters" },
                                required=True)
  
class ODPBackend(DefaultBackend):

    def get_form_class(self, request):
        return ODPRegistrationForm
    
    # also possible to catch signal to allow not having to 
    # mix profiles app and registration app
    # http://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
    # but since we are already extending registration
    # through a custom backend why not...
    @transaction.commit_on_success
    def register(self, request, **kwargs):
        new_user = super(ODPBackend,self).register(request, **kwargs)
        new_user.first_name = kwargs['first_name']
        new_user.last_name = kwargs['last_name']
        new_user.save()
        return new_user

