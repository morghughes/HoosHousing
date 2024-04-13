from django.db import models

from django.conf import settings
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_site_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    report_comment = models.CharField(max_length=1000)
    report_title = models.CharField(max_length=60, default='')
    upvotes = models.IntegerField(default=0)

    upvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_reports')

    LOCATION_POSSIBILITIES = [
        ("Balz-Dobie", "Balz-Dobie"), ("Cauthen", "Cauthen"), ("Gibbons", "Gibbons"), ("Kellogg", "Kellogg"),
        ("Lile-Maupin", "Lile-Maupin"), ("Shannon", "Shannon"), ("Tuttle-Dunnington", "Tuttle-Dunnington"),
        ("Watson-Webb", "Watson-Webb"), ("Woody", "Woody"), ("Courtenay", "Courtenay"), ("Dunglison", "Dunglison"),
        ("Fitzhugh", "Fitzhugh"), ("Brown College", "Brown College"), ("Gooch", "Gooch"), ("Dillard", "Dillard"),
        ("Hereford College", "Hereford College"), ("International Residential College", "International Residential College"),
        ("Bonnycastle", "Bonnycastle"), ("Dabney", "Dabney"), ("Echols", "Echols"), ("Emmet", "Emmet"),
        ("Hancock", "Hancock"), ("Humphreys", "Humphreys"), ("Kent", "Kent"), ("Lefevre", "Lefevre"), ("Metcalf", "Metcalf"), ("Page", "Page"),
        ("Bice", "Bice"), ("Bond", "Bond"),("Copeley", "Copeley"),("Faulkner", "Faulkner"),("Lambeth", "Lambeth"),(" French House", "French House"),
        ("Spanish House", "Spanish House"), ("Shea House", "Shea House"),
    ]
    report_location = models.CharField(max_length=250, choices=LOCATION_POSSIBILITIES, default="Balz-Dobie")
    report_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    report_response = models.TextField(null=True, blank=True)

    NEW = 'New'
    IN_PROGRESS = 'In Progress'
    COMPLETE = 'Complete'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETE, 'Complete'),
    ]
    report_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)

    NOISE = "Noise"
    MAINTENANCE = "Maintenance"
    SANITATION = "Sanitation"
    OTHER = "Other"

    TYPE_CHOICES = [
        (NOISE, 'Noise'),
        (MAINTENANCE, 'Maintenance'),
        (SANITATION, 'Sanitation'),
        (OTHER, 'Other')
    ]
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)

    is_public = models.BooleanField(default=False, verbose_name="Make report public")
    public_description = models.BooleanField(default=False, verbose_name="Public Description")
    public_files = models.BooleanField(default=False, verbose_name="Public Files")

    def __str__(self):
        return self.report_title


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# resources:
# https://docs.djangoproject.com/en/3.2/topics/db/models/
# https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
# https://docs.djangoproject.com/en/5.0/intro/tutorial02/


class FileUpload(models.Model):
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='file_uploads', on_delete=models.CASCADE, null=True, blank=True)
    data = models.FileField(upload_to='user_uploads/', null=True)
    time_added = models.DateTimeField(auto_now_add=True)
    # added to ensure that FileUploads are associated with particular Reports
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='uploads', null=True, blank=True)

    class Meta:
        verbose_name_plural = "File Uploads"

    def __str__(self):
        return f"{'Anonymous' if not self.uploader else self.uploader.get_username()} uploaded {self.data.name}"


@receiver(post_save, sender=get_user_model())
def ensure_user_profile_exists(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()
