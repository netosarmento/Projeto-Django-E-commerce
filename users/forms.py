from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Profile
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email...')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está sendo usado.')
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
        
        
 # form password reset
 
class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        """
        Substitui o envio de e-mail padrão para garantir que usamos o template customizado.
        """
        body = render_to_string(email_template_name, context)
        send_mail("Redefinição de senha - Nome Empresa", body, from_email, [to_email])       
        

# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes