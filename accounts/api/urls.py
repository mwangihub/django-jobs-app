from django.urls import path, include
from rest_framework import routers
from . import rest_views

app_name = "api_user"

'''
innovest-api/ ^all-users/$ [name='user-list']
innovest-api/ ^all-users/(?P<pk>[^/.]+)/$ [name='user-detail']
innovest-api/ ^employee-create/$ [name='user-list'] 
'''

router = routers.DefaultRouter()
router.register(r'all-users', rest_views.UsersViewSet)
router.register(r'employee-create', rest_views.EmployeeSignUpViewSet)
urlpatterns = [
    path('api/accounts/activate/<uidb64>/<token>/', rest_views.confirm_account, name='api-activate-account'),
]

urlpatterns += router.urls