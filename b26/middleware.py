from django.shortcuts import redirect
from django.urls import reverse

class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        just_logged_in = request.session.pop('just_logged_in', False)
        if just_logged_in and request.user.is_authenticated and hasattr(request.user, 'userprofile'):
            if request.user.userprofile.is_site_admin:
                return redirect('view_reports')
        return self.get_response(request)