from django.contrib.auth import views as auth_views
from django.urls import path
from . import auth_view as views


urlpatterns = [ 
    path('accounts/user_login/', views.UserLoginView.as_view(template_name='registration/login.html'), name="user_login"),
    
    path('accounts/sign-up/', views.SignUpViewMain.as_view(), name="sign-up"),
    path('accounts/register/employee', views.EmployeeSignUpView.as_view(), name="register-employee"),
    path('accounts/register/cutomer', views.CustomerSignUpView.as_view(), name="register-cutomer"),

    path('accounts/register/', views.SignUpView.as_view(), name="register"),
    

   
    path('accounts/logout/', views.UserLogoutView.as_view(), name="logout"),
    path('accounts/reset_password_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('accounts/reset-password/', views.ResetPasswordRequestView.as_view(), name="reset-password"),
    path('accounts/activate/<uidb64>/<token>/', views.confirm_account, name='activate'),
]


