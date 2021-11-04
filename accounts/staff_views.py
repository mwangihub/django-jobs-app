from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views import View
from . import forms
from . import models as _db
from jobs import models as j_db
from core.decorators import staff_required


User = get_user_model()


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class StaffAdminProfilePreView(View):
    template_name = "profiles/staff/profile_preview.html"
    form_class = None

    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, self.template_name, context)


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class StaffCreateView(generic.CreateView):
    model = j_db.Job
    template_name = "profiles/staff/create.html"
    form_class = forms.JobCreationForm
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        context = {
            'applications': j_db.JobsApplication.objects.all(),
            'j_form': self.form_class,
            'message': _db.InnovestUsersMessages.objects.all()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('segment'):
            form = self.form_class(request.POST or None, request.FILES or None)
            
            if form.is_valid():
                user = request.user
                title = form.cleaned_data.get('title')
                salary = form.cleaned_data.get('salary')
                location = form.cleaned_data.get('location')
                gender = form.cleaned_data.get('gender')
                required_age = form.cleaned_data.get('required_age')
                experience = form.cleaned_data.get('experience')
                description = form.cleaned_data.get('description')
                requirements = form.cleaned_data.get('requirements')
                positions = form.cleaned_data.get('positions')
                domain = get_current_site(request).domain
                j_db.Job.objects.create(
                        user=user,
                        title=title,
                        salary=salary,
                        location=location,
                        gender=gender,
                        required_age=required_age,
                        experience=experience,
                        description=description,
                        requirements=requirements,
                        positions=positions,
                        domain=domain
                    )
                
                messages.success(
                    request, f"Job created succesfully. we will be creating a preview mode of the job soon."
                )
                return redirect("user_urls:staff-create")
            else:
                context = {
                    'j_form': form
                }
                return render(request, self.template_name, context)


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class StaffProfileView(View):
    template_name = "profiles/staff/staff_view.html"
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.slug == kwargs['slug']:
            self.profile = get_object_or_404(
                _db.StaffProfile, user=request.user)
            return super(StaffProfileView, self).dispatch(request, *args, **kwargs)
        else:
            try:
                user = get_object_or_404(User, username=request.user.email)
                logout(request)
                return redirect('user_urls:user_login')
            except User.DoesNotExist:
                return redirect('user_urls:user_login')

    def get(self, request, *args, **kwargs):
        context = {
            'profile': self.profile,
            'fom': self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST, request.FILES, instance=self.profile)
        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.second_name = form.cleaned_data.get('second_name')
            profile.user.username = form.cleaned_data.get('username')
            profile.user.save()
            messages.success(request, 'Profile saved successfully')
        else:
            context = {
                'profile': self.profile,
                'segment': 'profile',
                'removeFooter': True,
                'form': form,

            }
            print(form.errors)
            messages.error(request, "There was an Error")
            return render(request, 'users/profile_edit.html', context)
        return redirect("user_urls:edit_profile", username=kwargs['username'])


# GENERAL VIEWS
class TermsAndConditionsView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'users/terms_conditions.html', context)


class PrivacyPolicyView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'users/privacy_policy.html', context)


class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'users/about_us.html', context)


class HowToApplyView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'users/how_apply.html', context)
