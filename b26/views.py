from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .models import FileUpload


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

        file_upload = FileUpload(data=file.name, uploader=request.user)
        file_upload.save()

        return JsonResponse({'file_url': file_url})
    else:
        return JsonResponse({'error': 'No file was given'}, status=400)


def admin_files(request):
    # checks to see if user is an admin
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized, please try again'}, status=403)

    # List all files (for simplicity; add pagination and filtering as needed)
    files = FileUpload.objects.all()
    files_data = [{'name': file.file.name, 'url': file.file.url}
                  for file in files]
    return JsonResponse({'files': files_data})


def welcome_view(request):
    return render(request, 'welcome.html')
