from django import forms
from . import models as _db
from jobs import models as j_db


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = _db.StaffProfile
        fields = '__all__'
        exclude = ['user']


class JobCreationForm(forms.ModelForm):
    segment = forms.CharField(widget=forms.HiddenInput())
    domain = forms.CharField(widget=forms.HiddenInput())
    no_applications = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(JobCreationForm, self).__init__(*args, **kwargs)
        self.fields['segment'].label = ""
        self.fields['segment'].widget.attrs['value'] = "create-job"
        self.fields['domain'].label = ""
        self.fields['domain'].widget.attrs['value'] = ""
        self.fields['no_applications'].label = ""

    class Meta:
        model = j_db.Job
        fields = '__all__'
        exclude = ['user', 'unique_key', 'taken', 'posted_on']



class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = _db.EmployeeProfile
        fields = '__all__'
        exclude = ['user']