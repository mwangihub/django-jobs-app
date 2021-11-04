from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .authentication.urls import urlpatterns as auth_urls
from accounts import staff_views
from accounts import employee_views

app_name = "user_urls"

urlpatterns = [
    # GENERAL URLS
    path("terms-and-conditions/",staff_views.TermsAndConditionsView.as_view(),name="terms-conditions",),
    path("how-to-apply/", staff_views.HowToApplyView.as_view(), name="how-to"),
    path("privacy-policy/",staff_views.PrivacyPolicyView.as_view(),name="privacy-policy",),
    path("about-us/meet-team/", staff_views.AboutUsView.as_view(), name="about-us"),

    # EMPLOYEE URLS
    path("employee/profile/<str:slug>/",employee_views.EmployeeProfileView.as_view(),name="employee-profile" ),



    # STAFF URLS
    path( "profile/staff/<str:slug>/",staff_views.StaffProfileView.as_view(),name="staff-profile"),
    path( "staff/create/all/",staff_views.StaffCreateView.as_view(),name="staff-create"),
    path( "staff/profile/preview/",staff_views.StaffAdminProfilePreView.as_view(),name="s-profile-prev"),
]
urlpatterns += auth_urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
