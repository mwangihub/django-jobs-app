'''
Application Programming Interface, which is a software intermediary that allows two \
applications to talk to each other. Each time you use an app like Facebook, \
send an instant message, or check the weather on your phone, you’re using an API.
'''
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('innovest.urls')),
    path('accounts/', include("accounts.urls")),
    path('jobs/', include('jobs.urls')),
    
    # Django-allauth
    path('accounts/', include('allauth.urls')),

    # Application Programming Interface
    path('rest-api/', include('rest_auth.urls')),
    path('innovest-api/', include('accounts.api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
