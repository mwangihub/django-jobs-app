import urllib
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic
from . import models as jobs_db
from . import forms

User = get_user_model()


class JobsPostsView(generic.ListView):
    model = jobs_db.Job
    template_name = "jobs/job_posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            user_applied_jobs = user.jobsapplication_set.all()
            context['applied'] = user_applied_jobs
            not_applied = jobs_db.Job.objects.not_applied(user)
            context['notapplied'] = not_applied
        else:
            context['notapplied'] = jobs_db.Job.objects.not_taken()
        return context


class JobDetailView(generic.DetailView):
    queryset = jobs_db.Job.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.JobsApplicationForm
        context["form"] = form
        if self.request.user.is_authenticated:
            if self.request.user.jobsapplication_set.filter(job_id=kwargs["object"].id).exists():
                context["applied"] = True
        return context

    def post(self, *args, **kwargs):
        try:
            job = jobs_db.Job.objects.by_id(slug=kwargs["slug"])
            form = forms.JobsApplicationForm(self.request.POST or None)
            if form.is_valid():
                user = self.request.user
                age = form.cleaned_data.get("age")
                phone = form.cleaned_data.get("phone")
                terms = form.cleaned_data.get("terms")
                if user.jobsapplication_set.filter(job_id=job.id).exists():
                    messages.warning(
                        self.request, f"You have already applied for this job"
                    )
                else:
                    jobs_db.JobsApplication.objects.create(
                        user=user, job=job, age=age, phone=phone, terms=terms
                    )
                    messages.success(self.request, f"Job application was successful")
        except jobs_db.Job.DoesNotExist:
            messages.warning(self.request, f"Invalid Url path.")
            return redirect("jobs:job-detail", slug=kwargs["slug"])
        else:
            return redirect("jobs:job-detail", slug=kwargs["slug"])
        # return redirect("jobs:job-detail", pk=job.id )
