from django import forms
from .models import *

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