from django.contrib.auth.signals import (user_logged_in, user_logged_out)
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from accounts import models as acc_db


@receiver(post_save, sender=acc_db.User, dispatch_uid='user_pre_signal_sender')
def user_pre_save_receiver(sender,  instance, created, **kwargs):
    value = f"{instance.first_name}-{instance.id}-{instance.second_name}"
    instance.slug = slugify(value, allow_unicode=False)
   

@receiver(post_save, sender=acc_db.User, dispatch_uid='user_signal_sender')
def user_post_save_receiver(sender,  instance, created, **kwargs):
    if created:
        if instance.is_employee:
            acc_db.EmployeeProfile.objects.create(user=instance)
            
        if instance.is_staff:
            acc_db.StaffProfile.objects.create(user=instance)