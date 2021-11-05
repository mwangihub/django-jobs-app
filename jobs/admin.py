from django.contrib import admin
from . import models as jobs_db


class AdminJobs(admin.ModelAdmin):
    list_display = (  "title",
         "user",
        "salary",
        "location",
        "gender",
        "required_age",
        "positions",
        "taken",
        "posted_on",
        'company_avatar',
    )


class AdminJobsApplication(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "phone",
        "applied_on",
        "terms",
    )


admin.site.register(jobs_db.Job, AdminJobs)
admin.site.register(jobs_db.JobsApplication, AdminJobsApplication)
