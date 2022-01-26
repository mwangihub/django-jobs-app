import uuid
from django.contrib.auth.signals import (user_logged_in, user_logged_out)
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from allauth.account.signals import user_signed_up
from accounts import models as acc_db


@receiver(pre_save, sender=acc_db.User, dispatch_uid='user_pre_signal_sender')
def user_pre_save_receiver(sender,  instance, **kwargs):
    # value = f"{instance.first_name}-{instance.second_name}-{uuid.uuid1()}"
    value = f"{instance.email}"
    instance.slug = slugify(value, allow_unicode=False)

@receiver(post_save, sender=acc_db.User, dispatch_uid='user_signal_sender')
def user_post_save_receiver(sender,  instance, created, **kwargs):
    if created:
        if instance.is_employee:
            profile = acc_db.EmployeeProfile.objects.create(user=instance)
            profile.save()
        if instance.is_staff:
            profile = acc_db.StaffProfile.objects.create(user=instance)
            profile.first_name = instance.first_name
            profile.second_name = instance.second_name
            profile.save()
            instance.save()
    if not created:
        if instance.is_staff:
            user = instance
            user.staff_profile.first_name = instance.first_name
            user.staff_profile.second_name = instance.second_name
            user.staff_profile.save()
        if instance.is_employee:
            db = acc_db.EmployeeProfile
            profile, created = db.objects.get_or_create(user=instance)
            profile.save()


@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):

    print(user.socialaccount_set.filter(
        provider=sociallogin.account.provider)[0].extra_data)
    user.active = True
    user.save()

    if sociallogin.account.provider == 'facebook':
        data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        picture_url = "http://graph.facebook.com/" + \
            sociallogin.account.uid + "/picture?type=large"
        email = data['email']
        first_name = data['first_name']

    # user.profile.avatar_url = picture_url
    # user.profile.email_address = email
    # user.profile.first_name = first_name
    # user.profile.save()
