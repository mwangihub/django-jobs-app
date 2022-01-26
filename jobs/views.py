import urllib
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic
from core.decorators import staff_required

from . import models as jobs_db
from . import forms

User = get_user_model()
@login_required
def remove_application(request, id):
    try:
        application = jobs_db.JobsApplication.objects.by_id(id=id)
        application.delete()
        messages.success(request,f'{application.job.title} removed succesfully')
    except jobs_db.JobsApplication.DoesNotExist:
        messages.warning(request,'This application do not exist')
    return redirect('user_urls:employee-profile', slug=request.user.slug )
    

class JobsPostsView(generic.ListView):
    model = jobs_db.Job
    template_name = "jobs/job_posts.html"

    def get(self, request, *args, **kwargs):
        # print(dir(request.user))
        return super().get(request, *args, **kwargs)
    
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
 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.JobsApplicationForm
        print(kwargs)
        context["form"] = form
        if self.request.user.is_authenticated:
            if self.request.user.jobsapplication_set.filter(job_id=kwargs["object"].id).exists():
                context["applied"] = True
        return context

    def post(self, *args, **kwargs):
        try:
            job = jobs_db.Job.objects.by_slug(slug=kwargs["slug"])
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
                    return redirect("jobs:job-detail", slug=kwargs["slug"])
                else:
                    jobs_db.JobsApplication.objects.create(
                        user=user, job=job, age=age, phone=phone, terms=terms
                    )
                    job.no_applications += 1
                    job.save()
                    messages.success(
                        self.request, f"Job application was successful")
                    return redirect("jobs:job-detail", slug=job.slug)
        except jobs_db.Job.DoesNotExist:
            messages.warning(self.request, f"Invalid Url path.")
            return redirect("jobs:job-detail", slug=kwargs["slug"])
        else:
            return redirect("jobs:job-detail", slug=kwargs["slug"])
        # return redirect("jobs:job-detail", pk=job.id )
