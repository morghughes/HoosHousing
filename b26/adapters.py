from allauth.account.adapter import DefaultAccountAdapter
from django.utils.text import slugify
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.shortcuts import redirect

class CustomAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        if user.email:
            username_base = user.email.split('@')[0]
            username = slugify(username_base)  # Makes username all lowercase and replaces spaces with hyphens
        else:
            username = request.POST.get('username', '')
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

    def save_user(self, request, user, form, commit=True):  # Saves users that sign in manually, with the custom,
        # optional first and last name fields
        user = super().save_user(request, user, form, commit=False)

        # Now handle the additional fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')

        if commit:
            user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        from allauth.account.models import EmailAddress

        if sociallogin.is_existing:  # if a matching social account already exists, just log the user into that
            return
        if 'email' in sociallogin.account.extra_data:  # if there is an email connected to  the current attempted
            # social login (should always be), then extract it, all lowercase
            email = sociallogin.account.extra_data['email'].lower()

            try:
                email_address = EmailAddress.objects.get(email=email)  # search list of emails, in database, entered
                # through both manual and Google signups, find email that matches current attempted social login
                user = email_address.user  # find user associated with email in database

                if not email_address.verified:  # if email is not already verified (i.e. manual signup attempting
                    # Google login for first time), then verify the email
                    email_address.verified = True
                    email_address.save()

                sociallogin.connect(request, user)  # connect new sociallogin/account to existing user with matching
                # email and login -- existing user now has a social account
                return perform_login(request, user, 'none')

            except EmailAddress.DoesNotExist:  # if no email matches sociallogin attempt email, then just go on
                # creating a branch new user and social account
                pass
