from django.conf import settings
from django.urls import path
from django.conf.urls import handler404
from django.conf.urls.static import static
from . import views

app_name = 'esign'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('save_pdf_to_db/', views.save_pdf_to_db, name='save_pdf_to_db'),
    path('management/<str:pk>/', views.management, name='management'),
    path('get_names_emails/', views.get_names_emails_for_company, name='get_names_emails'),
    path('detail/<str:pk>/', views.detail, name='detail'),
    path('sign/<str:pk>/', views.sign, name='sign'),
    path('check_session/', views.check_session, name='check_session'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "esign.views.handler404"  # Set the handler404 for the app