from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "username",  "position")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "username",  "position", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)

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