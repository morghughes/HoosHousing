from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.core.files.storage import default_storage
from django.http import JsonResponse

# Create your views here.
@login_required
def index(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'user_name': request.user.username,
            'is_site_admin': user_profile.is_site_admin,
        }
    except UserProfile.DoesNotExist:
        # Handle case where user profile does not exist, if necessary
        context = {
            'user_name': request.user.username,
            'is_site_admin': False,
        }

    return render(request, 'index.html', context)

# resources:
# https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.url(file_name)
        return JsonResponse({'file_url': file_url})
    return JsonResponse({'error': 'File not provided'}, status=400)
