from django.conf import settings
from django.urls import path
from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from . import views

app_name = 'esign'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('xlogin/', views.xlogin, name='xlogin'),
    path('login/', views.login_request, name='login'),
    path('resend_totp/', views.resend_totp, name='resend_totp'),
    path('verify_totp/', views.verify_totp, name='verify_totp'),

    path('logout/', views.logout_request, name='logout'),
    path('save_pdf_to_db/', views.save_pdf_to_db, name='save_pdf_to_db'),
    # path('add_signature_to_pdf/', views.add_signature_to_pdf, name='add_signature_to_pdf'),
    path('add_image_signature/', views.add_image_signature, name='add_image_signature'),

    path('management/<str:hashed_url>/', views.management, name='management'),
    path('update_document_title/<str:document_id>/', views.update_document_title, name='update_document_title'),
    path('update_permission/', views.update_permission, name='update_permission'),
    path('update_due/', views.update_due, name='update_due'),
    path('add_remark/', views.add_remark, name='add_remark'),

    path('get_names_emails/', views.get_names_emails_for_company, name='get_names_emails'),
    path('sign/<str:hashed_url>/', views.sign, name='sign'),
    path('check_session/', views.check_session, name='check_session'),


    # path('test/', views.test, name='test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "esign.views.handler403"  # Set the handler403 for the app
handler404 = "esign.views.handler404"  # Set the handler404 for the app
handler500 = "esign.views.handler500"  # Set the handler500 for the app