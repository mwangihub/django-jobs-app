from django.urls import path
from . import views

app_name = "jobs"
urlpatterns = [
    path("job-posts/", views.JobsPostsView.as_view(), name="job-posts"),
    path('job-detail/<str:slug>/', views.JobDetailView.as_view(), name='job-detail'),
]
