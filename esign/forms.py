from django import forms
from .models import *

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