"""
URL configuration for imghost project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from imghostapp import views
from imghostapp.views import UserGalleryView

from account.views import (
    register_view,
    login_view,
    logout_view,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

     # Password reset links
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/request/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_request.html'),
    name='password_reset_request'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_set.html'), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),

    # Adding image path
    path('upload/', views.upload_image, name='upload-image'),

    # Admin path
    path("admin/", admin.site.urls),

    # Gallery path
    path('gallery/<str:username>/', UserGalleryView.as_view(), name='user_gallery'),

    # Editing images
    path('image/delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('image/edit/<int:image_id>/', views.edit_image, name='edit_image'),

    #Downloading images
    path('download/<int:image_id>/', views.download_image, name='download_image')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)