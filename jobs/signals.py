from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models as _db
from accounts import models as acc_db
from core.methods import send_mass_mail


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
