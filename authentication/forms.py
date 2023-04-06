from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext as _


class Registration_Form(UserCreationForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(
        attrs={'class': '', 'placeholder': 'Password'}), required=False)
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput(
        attrs={'class': '', 'placeholder': 'Confirm Password'}), required=False)

    def __init__(self, *args, **kwargs):
        super(Registration_Form, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields.get('username').required = False

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email'),
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': '', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': '', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': '', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': '', 'placeholder': 'Email'}),
        }

        help_texts = {
            'username': ''
        }

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data.get('email')
        return self.cleaned_data

    def clean_first_name(self):
        inp_first_name = self.cleaned_data.get('first_name')
        if len(inp_first_name.strip()) == 0:
            raise ValidationError(_("Please Enter Your First Name!!"))
        return inp_first_name

    def clean_last_name(self):
        inp_last_name = self.cleaned_data.get('last_name')
        if len(inp_last_name.strip()) == 0:
            raise ValidationError(_("Please Enter Your Last Name!!"))
        return inp_last_name

    def clean_email(self):
        inp_email = self.cleaned_data.get('email')
        validator = EmailValidator(_("Please Provide Valid Email!!"))
        validator(inp_email)
        if User.objects.filter(email=inp_email).exists():
            raise ValidationError(_(f"{inp_email} is Already Exists!!"))
        return inp_email

    def clean_password1(self):
        inp_password1 = self.cleaned_data.get('password1')
        if len(inp_password1) == 0:
            raise ValidationError(_("Please Enter The Password!!"))
        return inp_password1

    def clean_password2(self):
        inp_password2 = self.cleaned_data.get('password2')
        inp_password1 = self.data.get('password1')
        if len(inp_password2) == 0:
            raise ValidationError(_("Please Confirm Your Password!!"))
        if inp_password1 != inp_password2:
            raise ValidationError(_("Password Must Matched!!"))
        return inp_password2
