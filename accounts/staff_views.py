from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import fields
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from . import forms
from . import models as _db
from jobs import models as j_db
from core.decorators import staff_required, non_required


User = get_user_model()


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class JobUpdateView(generic.UpdateView):
    model = j_db.Job
    template_name = "profiles/staff/job_update.html"
    fields = [
        "title",
        "salary",
        "company_avatar",
        "location",
        "gender",
        "required_age",
        "positions",
        "experience",
        "description",
        "requirements", ]

    def get_success_url(self) -> str:
        return reverse_lazy('user_urls:job-prev', kwargs={'slug': self.object.slug})


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class JobPreView(generic.DetailView):
    model = j_db.Job
    template_name = "profiles/staff/job_preview.html"


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class AdminProfilePreView(View):
    template_name = "profiles/staff/profile_preview.html"
    form_class = None

    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, self.template_name, context)


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class ApplicationsView(View):
    template_name = "profiles/staff/list_applications.html"
    form_class = None

    def get(self, request, *args, **kwargs):
        context = {
            'applications': j_db.JobsApplication.objects.all(),
        }
        return render(request, self.template_name, context)


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class ApplicantUsersView(View):
    template_name = "profiles/staff/list_applicant_users.html"

    def get(self, request, *args, **kwargs):
        context = {
            'applicants': _db.User.objects.employee_user(),
        }
        return render(request, self.template_name, context)


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class StaffUsersView(View):
    template_name = "profiles/staff/list_staff_users.html"

    def get(self, request, *args, **kwargs):
        staff = _db.User.objects.staff_user().exclude(id=request.user.id)
        context = {
            'staffs': staff,
        }
        return render(request, self.template_name, context)


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class InnovestMessagesView(View):
    template_name = "profiles/staff/list_web_messages.html"

    def get(self, request, *args, **kwargs):
        context = {
            'mess': _db.InnovestUsersMessages.objects.all(),
        }
        return render(request, self.template_name, context)


@method_decorator([login_required(login_url='user_urls:user_login'), staff_required], name='dispatch')
class CreateJobsView(generic.CreateView):
    model = j_db.Job
    template_name = "profiles/staff/create.html"
    form_class = forms.JobCreationForm
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        context = {
            'j_form': self.form_class,
            'job_list': j_db.Job.objects.all()
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
class ProfileView(View):
    template_name = "profiles/staff/staff_view.html"
    form_class = forms.StaffProfileForm
    profile = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.slug == kwargs['slug']:
            self.profile = get_object_or_404(
                _db.StaffProfile, user=request.user)
            return super(ProfileView, self).dispatch(request, *args, **kwargs)
        else:
            try:
                user = get_object_or_404(
                    User, slug=request.user.kwargs['slug'])
                logout(request)
                return redirect('user_urls:user_login')
            except User.DoesNotExist:
                return redirect('user_urls:user_login')

    def get(self, request, *args, **kwargs):
        context = {
            'profile': self.profile,
            'p_form': self.form_class(instance=self.profile),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None,
                               request.FILES or None, instance=self.profile)
        print(request.POST)
        if form.is_valid():
            form.save()
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.second_name = form.cleaned_data.get('second_name')
            profile.user.username = form.cleaned_data.get('username')
            profile.user.save()
            messages.success(request, 'Profile saved successfully')
            return redirect("user_urls:staff-profile", slug=kwargs['slug'])
        else:
            context = {
                'profile': self.profile,
                'segment': 'profile',
                'removeFooter': True,
                'form': form,
            }
            messages.error(request, "There was an Error")
            return render(request, self.template_name, context)


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


@method_decorator([login_required(login_url="home"), non_required, ], name="dispatch",)
class ChooseUserTypeView(generic.View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "registration/choose_user_type.html", context)

    def post(self, request, *args, **kwargs):
        u_type = str(request.POST['type'])
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            user = None
        if user is not None:
            context = {
                "selected": f"You have choosen {u_type} account",
            }
            if hasattr(user, u_type):
                if u_type != 'staff' and u_type != 'none':
                    setattr(user, u_type, True)
                    user.non = False
                    user.save()
                    context["title"] = f"Welcome to {u_type} Account"
                    return redirect("/")
                else:
                    if u_type == 'staff':
                        return redirect("user_urls:staff_register")
            if u_type == 'none':
                none = "You have to select one of the existing accounts"
                context["selected"] = none
                return render(request, "registration/choose_user_type.html", context)
        else:
            context = {
                "selected": f"Your account was not created!",
            }
            return render(request, "registration/choose_user_type.html", context)


class StaffRegisterProcessView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/staff_reg_process.html')
