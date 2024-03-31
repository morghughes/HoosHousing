from django.shortcuts import render, get_object_or_404
from .models import Report
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import UserProfile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .models import FileUpload
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
import random


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

class ReportView(generic.DetailView):
    model = Report
    template_name = "report.html"
    context_object_name = 'report'

class SubmittedView(TemplateView):
    model = Report
    template_name = "submitted.html"

# class CustomLoginView(LoginView):
#     def get_redirect_url(self):
#         user = self.request.user
#         if user.is_authenticated:
#             if user.userprofile.is_site_admin:
#                 return reverse('admin_files') # redirect site admins straight to page with all the reports
#             else:
#                 return reverse('index') # redirect normal users to the index page
#         return super().get_redirect_url()


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


# def admin_files(request):
#     # checks to see if user is an admin
#     if not request.user.is_staff:
#         return JsonResponse({'error': 'Unauthorized, please try again'}, status=403)

#     # List all files (for simplicity; add pagination and filtering as needed)
#     files = FileUpload.objects.all()
#     files_data = [{'name': file.file.name, 'url': file.file.url}
#                   for file in files]
#     return JsonResponse({'files': files_data})
def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, 'report_detail.html', {'report': report})

def view_reports(request):
    if request.user.userprofile.is_site_admin:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(report_user=request.user.userprofile)
    return render(request, 'admin_files.html', {'reports': reports})

def welcome_view(request):
    return render(request, 'welcome.html')

def report_view(request):
    return render(request, 'report.html')

def submit(request):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        location = request.POST.get("location", "")
        files = request.FILES.getlist('files')
        # if 'file' in request.FILES:
        #     file = request.FILES['file']
        # else:
        #     file = None
        # comment = request.POST.get("comment", "")
        # location = request.POST.get("location", "")
        if not comment or not location or not files:
            return render(
                request,
                "report.html",
                {
                    "error_message": "Please enter a location, describe what you're reporting, and submit a valid image/pdf."
                }
            )
        else:
            if request.user.is_authenticated:
                current_user = UserProfile.objects.get(user=request.user)
                report = Report.objects.create(report_comment=comment, report_location=location, report_user=current_user)
            else:
                report = Report.objects.create(report_comment=comment, report_location=location, report_user=None)
            report.save()

            for file in files:
                FileUpload.objects.create(data=file, uploader=request.user, report=report)

            return HttpResponseRedirect(reverse("submitted"))