from django.urls import path
from . import views
app_name = 'innovesthome'
urlpatterns = [
   path('', views.InnovestHomeView.as_view(), name='innovest-home'),
   path('contact/ask-question/', views.ContactRedirectView.as_view(), name='ask-question'),
]