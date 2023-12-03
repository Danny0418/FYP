from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class LoginForm(forms.Form):
    UID = forms.CharField(max_length=100)
    psw = forms.CharField(widget=forms.PasswordInput)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title','pdf_file')

class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ('docID','signature')

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('orgID','name','email','address','phone_no')

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "username", "orgID", "position")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)