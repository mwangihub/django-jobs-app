from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import models
from django.db.models import fields
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views import View
from . import forms
from . import models as acc_db
from jobs import models as job_db
from core.decorators import employee_required

User = get_user_model()


@method_decorator([login_required(login_url="user_urls:user_login"), employee_required], name="dispatch",)
class EmployeeApplicationUpdateView(generic.UpdateView):
    model = job_db.JobsApplication
    template_name = 'profiles/employee/app_update.html'
    fields = ['phone', 'age']

    def get_success_url(self) -> str:
        return reverse_lazy("user_urls:my-app")


@method_decorator([login_required(login_url="user_urls:user_login"), employee_required], name="dispatch",)
class EmployeeMyApplicationsView(generic.TemplateView):
    template_name = 'profiles/employee/my_applications.html'

    def get(self, request, *args, **kwargs):
        context = {
            'jobs': job_db.JobsApplication.objects.applied(request.user)
        }
        return render(request, self.template_name, context)




@method_decorator([login_required(login_url="user_urls:user_login"), employee_required], name="dispatch",)
class EmployeeProfileView(View):
    profile = None
    form_class = forms.EmployeeProfileForm
    template_name = 'profiles/employee/profile_view.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.slug == kwargs['slug']:
            self.profile = get_object_or_404(
                acc_db.EmployeeProfile, user=request.user)
        return super(EmployeeProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'profile': self.profile,
            'form': self.form_class(instance=request.user.employee_profile),
            'jobs': job_db.JobsApplication.objects.applied(request.user)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None,
                               request.FILES or None, instance=self.profile)
        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.second_name = form.cleaned_data.get('second_name')
            profile.user.save()
            messages.success(request, 'Profile saved successfully')
        else:
            context = {
                'profile': self.profile,
                'form': form,
            }
            messages.error(request, "There was an Error")
            return render(request, self.template_name, context)
        return redirect("user_urls:employee-profile", slug=kwargs['slug'])
