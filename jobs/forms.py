from django import forms
from . import models as jobs_db


class JobsApplicationForm(forms.ModelForm):
    terms = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={"class": " form-check-input ms-0", "checked": "checked"}
        ),
        label="",
        help_text="Accept our terms and conditions",
    )

    def __init__(self, *args, **kwargs):
        super(JobsApplicationForm, self).__init__(*args, **kwargs)
        self.fields['age'].widget.attrs['min'] = 25
        self.fields['age'].widget.attrs['max'] = 40

    class Meta:
        model = jobs_db.JobsApplication
        fields = "__all__"
        exclude = ["user", "job"]
