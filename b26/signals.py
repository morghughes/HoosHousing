from django.dispatch import receiver
from allauth.account.signals import user_logged_in

@receiver(user_logged_in)
def set_just_logged_in_flag(sender, request, user, **kwargs):
    request.session['just_logged_in'] = True