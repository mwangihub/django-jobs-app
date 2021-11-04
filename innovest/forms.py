from django import forms
from django.forms import fields
from accounts import models as acc_db

class InnovestSubscribeForm(forms.ModelForm):
    subscribe = forms.CharField(widget=forms.HiddenInput())
    active = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = acc_db.InnovestSubcribers
        fields = '__all__'

class InnovestMessagesForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
        label="",
    )
    names = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your names"}
        ),
        label="",
        help_text="Not required"
    )
    inform_us = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Message",
                "rows": 4,
                "cols": 15,
            }
        ),
        label="",
    )
    session_user = forms.CharField(widget=forms.HiddenInput())
    message = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = acc_db.InnovestUsersMessages
        fields = "__all__"

    
