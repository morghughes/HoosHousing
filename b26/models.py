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
    report_comment = models.CharField(max_length=1000)
    report_location = models.CharField(max_length=100)
    report_file = models.FileField()
    report_user = UserProfile()
    def __str__(self):
        return self.report_comment


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

    def __str__(self):
        return f"{'Anonymous' if not self.uploader else self.uploader.get_username()} uploaded {self.data.name}"


@receiver(post_save, sender=get_user_model())
def ensure_user_profile_exists(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()
