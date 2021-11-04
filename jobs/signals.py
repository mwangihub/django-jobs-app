from django.conf import settings
# from django.core.mail import send_mass_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models as _db
from accounts import models as acc_db


def get_rendered_html(template_name, context={}):
    html_content = render_to_string(template_name, context)
    return html_content


def send_email(subject, html_content, text_content=None, from_email=None, recipients=[], attachments=[], bcc=[], cc=[]):
    # send email to user with attachment
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL
    if not text_content:
        text_content = ''
    email = EmailMultiAlternatives(
        subject, text_content, from_email, recipients, bcc=bcc, cc=cc
    )
    email.attach_alternative(html_content, "text/html")
    for attachment in attachments:
        # Example: email.attach('design.png', img_data, 'image/png')
        email.attach(*attachment)
    email.send()


def send_mass_mail(data_list):
    for data in data_list:
        template = data.pop('template')
        context = data.pop('context')
        html_content = get_rendered_html(template, context)
        data.update({'html_content': html_content})
        send_email(**data)


@receiver(post_save, sender=_db.Job, dispatch_uid='job_signal_sender')
def job_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        admins, subscribers = [], []
        for sub in acc_db.InnovestSubcribers.objects.all():
            subscribers.append(sub.email)
        for admin in acc_db.User.objects.staff_user():
            admins.append(admin.email)
        sub_message = {
            'subject': 'Innovest New job posted',
            'recipients': subscribers,
            'template': "profiles/staff/email_job_posted.html",
            'context': {'job': instance, }
        }

        admin_message = {
            'subject': 'Innovest admin messages',
            'recipients': admins,
            'template': "profiles/staff/email_to_admins_job_posted.html",
            'context': {'job': instance, }
        }
        send_mass_mail([sub_message, admin_message])
