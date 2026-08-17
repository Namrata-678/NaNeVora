from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Admin Panel
    path('admin/', admin.site.urls),

    # Website App
    path('', include('website.urls')),

    # # Google Login (django-allauth)
    path('accounts/', include('allauth.urls')),

]




# Serve Media Files During Development

if settings.DEBUG:

    urlpatterns += static(

        settings.MEDIA_URL,

        document_root=settings.MEDIA_ROOT

    )