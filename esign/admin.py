from django.contrib import admin
from .models import *

# Register your models here.

class DocumentAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {"fields": ["title", "pdf_file"]}),
    #     ("Date information", {"fields": ["content"]}),
    # ]
    list_display = ('title','pdf_filename')

    # Custom method to display PDF file name
    def pdf_filename(self, obj):
        return obj.pdf_file.name.split('/')[-1]

    pdf_filename.short_description = 'PDF File Name'  # Custom column header

class SignatureAdmin(admin.ModelAdmin):
    list_display = ('docID', 'signature', 'signed_at')

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('orgID','name','email','address','phone_no')


admin.site.register(Document, DocumentAdmin)
admin.site.register(Signature, SignatureAdmin)
admin.site.register(Organization, OrganizationAdmin)