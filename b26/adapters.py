from allauth.account.adapter import DefaultAccountAdapter
from django.utils.text import slugify

class CustomAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        username_base = user.email.split('@')[0]
        username = slugify(username_base)  # Makes username all lowercase and replaces spaces with hyphens
        count = 0

        while True:
            if count == 0:
                proposed_username = username
            else:
                proposed_username = f"{username}{count}"
            if not self.username_exists(proposed_username):  # If the username exists, up the count so that a number
                # can be added to the end of the username
                break
            count += 1

        user.username = proposed_username

    def username_exists(self, username):
        from allauth.account.models import EmailAddress
        return EmailAddress.objects.filter(user__username=username).exists()