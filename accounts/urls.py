

from django.urls import path
from . import staff_views
from . import employee_views
from .authentication.urls import urlpatterns as auth_urls



app_name = "user_urls"

urlpatterns = [
    # GENERAL URLS
    path("terms-and-conditions/",
         staff_views.TermsAndConditionsView.as_view(), name="terms-conditions",),
    path("choose-user/",
         staff_views.ChooseUserTypeView.as_view(), name="choose-user",),
    path("staff-register/",
         staff_views.StaffRegisterProcessView.as_view(), name="staff_register",),
    path("how-to-apply/", staff_views.HowToApplyView.as_view(), name="how-to"),
    path("privacy-policy/", staff_views.PrivacyPolicyView.as_view(),
         name="privacy-policy",),
    path("about-us/meet-team/", staff_views.AboutUsView.as_view(), name="about-us"),

    # EMPLOYEE URLS
    path("employee/profile/<str:slug>/",
         employee_views.EmployeeProfileView.as_view(), name="employee-profile"),
    path("employee/update-application/<int:pk>/",
         employee_views.EmployeeApplicationUpdateView.as_view(), name="ed-application"),
    path("employee/my-application/all/",employee_views.EmployeeMyApplicationsView.as_view(), name="my-app"),

    # STAFF URLS
    path("profile/staff/<str:slug>/",
         staff_views.ProfileView.as_view(), name="staff-profile"),
    path("staff/create/all/", staff_views.CreateJobsView.as_view(), name="staff-create"),
    path("staff/profile/preview/",
         staff_views.AdminProfilePreView.as_view(), name="s-profile-prev"),
    path("staff/applications/all/",
         staff_views.ApplicationsView.as_view(), name="all-apps"),
    path("staff/applicants/all/",
         staff_views.ApplicantUsersView.as_view(), name="applicants"),
    path("staff/staff-users/all/",
         staff_views.StaffUsersView.as_view(), name="staff"),
    path("staff/web-messages/all/",
         staff_views.InnovestMessagesView.as_view(), name="web-messages"),
    path("staff/job/preview/<slug:slug>/",
         staff_views.JobPreView.as_view(), name="job-prev"),
    path("staff/job/update/<slug:slug>/",
         staff_views.JobUpdateView.as_view(), name="job-update"),
]
urlpatterns += auth_urls