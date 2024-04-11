from django.shortcuts import render, get_object_or_404, redirect
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
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.messages import constants as message_constants
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

def update_resolution(request, report_id):
    if not (request.user.is_authenticated and request.user.userprofile.is_site_admin):
        return redirect('some_error_page')

    report = get_object_or_404(Report, pk=report_id)
    if request.method == "POST":
        report_response = request.POST.get("report_response", "")
        if report_response:
            report.report_response = report_response
            report.save()
            messages.add_message(request, message_constants.SUCCESS, "Resolution details updated successfully.", extra_tags='resolution_update')
            return redirect('report_detail', report_id=report_id)
    return redirect('report_detail', report_id=report_id)

@require_POST
def mark_report_complete(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.user.is_authenticated and request.user.userprofile.is_site_admin:
        # Check if the checkbox was checked or not
        if 'completeStatus' in request.POST:
            report.report_status = 'Complete'
        else:
            report.report_status = 'In Progress'  # Or any other default status
        report.save()
    return HttpResponseRedirect(reverse('report_detail', args=[report_id]))

def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.user.is_authenticated and request.user.userprofile.is_site_admin:
        if report.report_status == Report.NEW:
            report.report_status = Report.IN_PROGRESS
            report.save()
    return render(request, 'report_detail.html', {'report': report})

def view_reports(request):
    all_reports = Report.objects.all()
    if not request.user.userprofile.is_site_admin:
        user_reports = all_reports.filter(report_user=request.user.userprofile)
    else:
        user_reports = all_reports

    return render(request, 'admin_files.html', {
        'all_reports': all_reports,
        'user_reports': user_reports,
    })


def welcome_view(request):
    return render(request, 'welcome.html')

def report_view(request):
    context = {
        'TYPE_CHOICES': Report.TYPE_CHOICES,
    }
    return render(request, 'report.html', context)

def submit(request):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        location = request.POST.get("location", "")
        type = request.POST.get("type", "")
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
                report = Report.objects.create(report_comment=comment, report_location=location, report_user=current_user, report_type=type)
            else:
                report = Report.objects.create(report_comment=comment, report_location=location, report_user=None, report_type=type)
            report.save()

            for file in files:
                FileUpload.objects.create(data=file, uploader=request.user, report=report)

            return HttpResponseRedirect(reverse("submitted"))