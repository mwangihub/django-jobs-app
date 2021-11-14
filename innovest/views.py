from django.shortcuts import redirect, render
from django.views import generic
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from accounts import models as acc_db
from jobs import models as jobs_db
from . import forms



class InnovestHomeView(generic.View):
    def get(self, request, *args, **kwargs):
        context = {
            "form_msg": forms.InnovestMessagesForm(
                initial={"session_user": request.user.email
                         if request.user.is_authenticated else "Annonymous User",
                         "message": "Innovest subscriber",
                         }
            ),
            "form_sub": forms.InnovestSubscribeForm(
                initial={"subscribe": "Innovest subscriber", }
            ),
            "jobs": jobs_db.Job.objects.not_taken()[:4]
        }
        return render(request, "innovesthome/innovesthome.html", context)

    def post(self, request, *args, **kwargs):
        if request.POST.get("message"):
            form_msg = forms.InnovestMessagesForm(request.POST or None)
            if form_msg.is_valid():
                subject = "New message from innovest"
                message = form_msg.cleaned_data.get("inform_us")
                from_email = form_msg.cleaned_data.get("email")
                from_name = {form_msg.cleaned_data.get("names")}
                message += f"\nFrom: Email:{from_email}\nname:{from_name}"
                to_email = [
                    "pmwangij9@gmail.com", "njeriephie@gmail.com"
                ]
                send_mail(subject, message, settings.EMAIL_HOST_USER, to_email)
                messages.success(
                    request,
                    f"We have received your message. We will be giving you feedback soon",
                )
                form_msg.save()
                return redirect("innovesthome:innovest-home")
            else:
                context = {"form": form_msg.errors}
                messages.success(request, f"Something went wrong.")
                return render(request, "innovesthome/innovesthome.html", context)

        if request.POST.get("subscribe"):
            form_sub = forms.InnovestSubscribeForm(request.POST or None)
            if form_sub.is_valid():
                subject = "New job subscriber"
                from_email = form_sub.cleaned_data.get("email")
                message = f"{from_email} has subscribe in the website to be \
                    informed about new jobs.\n"
                to_email = [
                    "pmwangij9@gmail.com", "njeriephie@gmail.com"
                ]
                send_mail(subject, message, settings.EMAIL_HOST_USER, to_email)
                messages.success(
                    request,
                    f"You have succefully subscribe for new jobs mails.",
                )
                form_sub.save()
                return redirect("innovesthome:innovest-home")
            else:
                context = {"form": form_sub.errors}
                messages.success(request, f"Something went wrong.")
                return render(request, "innovesthome/innovesthome.html", context)

        return redirect("innovesthome:innovest-home")


class ContactRedirectView(generic.RedirectView):
    def get_redirect_url(*args, **kwargs):
        return reverse("innovesthome:innovest-home") + f"#{'contact'}"