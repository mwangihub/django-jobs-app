import uuid
from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.utils.text import slugify

User = get_user_model()
from django.core.validators import MaxValueValidator, MinValueValidator


class JobsManager(models.Manager):
    def already_taken(self):
        qs = self.get_queryset().filter(taken=True)
        return qs

    def by_id(self, id):
        qs = self.get_queryset().get(id=id)
        return qs

    def not_applied(self, user):
        ids = []
        for applied_job in user.jobsapplication_set.all():
            for job in self.not_taken():
                if job == applied_job.job:
                    ids.append(job.id)
        qs = self.get_queryset().exclude(id__in=ids)
        return qs

    def not_taken(self):
        qs = self.get_queryset().filter(taken=False)
        return qs

    def by_user(self, user):
        qs = self.get_queryset().filter(user=user)
        return qs


class GenderChoice(models.TextChoices):
    MALE = "m", "Male only"
    FEMALE = "f", "Female only"
    ANY = "a", "Any gender preffered"


class Job(models.Model):
    GENDER = GenderChoice.choices
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="created_by")
    unique_key = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=250)
    salary = models.CharField(
        max_length=150,
        verbose_name="proposed pay",
        help_text="use 150 words to describe the the pay",
    )
    company_avatar = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    location = models.CharField(max_length=50)
    gender = models.CharField(
        choices=GenderChoice.choices, max_length=1, default=GenderChoice.ANY
    )
    required_age = models.IntegerField(default=25)
    experience = RichTextField(
        max_length=2000,
        default="Prior experience is an added advantage.",
        help_text=("Use 2000 words"),
    )
    description = RichTextField(
        max_length=2000, help_text="Use 2000 words only", blank=False, null=False
    )
    requirements = RichTextField(
        max_length=2000, help_text="Use 2000 words only.", null=True, blank=True
    )
    slug = models.SlugField(
        default=uuid.uuid4, editable=False, null=True, blank=True, max_length=250
    )
    segment = models.CharField(
        default="create-job", max_length=10
    )
    domain = models.CharField(max_length=250)
    positions = models.IntegerField(default=1)
    taken = models.BooleanField(default=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    objects = JobsManager()

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.title

    @property
    def is_taken(self):
        return self.taken

    def save(self, *args, **kwargs):
        value = f"{self.title}-{uuid.uuid1()}-{self.location}"
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class JobsApplicationManager(models.Manager):
    def selected(self, user):
        qs = self.get_queryset().filter(selected=True, user=user)
        return qs

    def applied(self, user):
        qs = self.get_queryset().filter(user=user)
        return qs


class JobsApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="applied_by")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applied_job")
    phone = models.CharField(
        max_length=32, verbose_name="Phone", help_text="Fomart (+123 456 789 1234)"
    )
    age = models.IntegerField(
        default=25,
        validators=[MaxValueValidator(40), MinValueValidator(25)],
        help_text="Minimum required age is 25 years",
    )
    applied_on = models.DateTimeField(auto_now_add=True)
    terms = models.BooleanField(default=True, verbose_name="Accept terms")
    selected = models.BooleanField(default=False, verbose_name="Selected for interview")

    objects = JobsApplicationManager()

    def __str__(self):
        return self.job.title

    #     phone = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={ "placeholder": "Phone number"}
    #     ),
    #     label="Your phone number",
    #     help_text="+123 456 789 1234",
    # )
