from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from .models import FileUpload, Report, UserProfile
from django.db.models import Q
from django.views import generic
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.messages import constants as message_constants


def welcome_view(request):
    return render(request, 'welcome.html')


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


@login_required
def update_resolution(request, report_id):
    if not (request.user.is_authenticated and request.user.userprofile.is_site_admin):
        return HttpResponseForbidden('You do not have permission to perform this action.')

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


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.user.is_authenticated and request.user.userprofile.is_site_admin:
        if report.report_status == Report.NEW:
            report.report_status = Report.IN_PROGRESS
            report.save()
    return render(request, 'report_detail.html', {'report': report})


@login_required
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


def signin_view(request):
    return render(request, 'login.html')


def report_view(request):
    context = {
        'TYPE_CHOICES': Report.TYPE_CHOICES,
        'LOCATION_POSSIBILITIES': Report.LOCATION_POSSIBILITIES,
        'location': '',
        'type': '',
        'title': '',
        'comment': '',
        'is_public': False,
        'public_description': False,
        'public_files': False
    }
    return render(request, 'report.html', context)


def submit(request):
    context = {
        'LOCATION_POSSIBILITIES': Report.LOCATION_POSSIBILITIES,
        'TYPE_CHOICES': Report.TYPE_CHOICES,
        'location': '',
        'type': '',
        'title': '',
        'comment': '',
        'is_public': False,
        'public_description': False,
        'public_files': False
    }

    if request.method == 'POST':
        if request.POST.get('action') == 'cancel':
            return HttpResponseRedirect(request.POST.get('cancel_redirect', '/'))

        context.update({
            'location': request.POST.get("location", ""),
            'type': request.POST.get("type", ""),
            'title': request.POST.get("title", ""),
            'comment': request.POST.get("comment", ""),
            'is_public': request.POST.get('is_public') == 'on',
            'public_description': request.POST.get('public_description') == 'on',
            'public_files': request.POST.get('public_files') == 'on',
        })

        files = request.FILES.getlist('files')
        total_size = sum(file.size for file in files)

        if not context['comment'] or not context['location'] or not context['title'] or not context['type']:
            messages.error(request, "Please ensure all fields not noted as 'Optional' are answered. You are not required to select any checkboxes.", extra_tags='form_error')
        elif not context['is_public'] and (context['public_description'] or context['public_files']):
            messages.error(request, "You cannot share your description and/or files if the overall privacy is still private.", extra_tags='form_error')
        elif not files and context['public_files']:
            messages.error(request, "If you would like you would like to make your files public to other non-admin users, please select a file or files to upload.", extra_tags='form_error')
        elif len(files) > 5:
            messages.error(request, "You cannot upload more than 5 files.", extra_tags='form_error')
        elif total_size > 52428800:  # 50 MB
            messages.error(request, "The total size of the files cannot exceed 50 MB.", extra_tags='form_error')

        else:
            similar_reports = Report.objects.filter(
                Q(report_type=context['type']) & Q(report_location=context['location']) & ~Q(report_status='Complete') & Q(is_public=True)
            )
            title_words = context['title'].split()
            if len(similar_reports) != 0:
                for similar in similar_reports:
                    counter = 0
                    similar_words = similar.report_title.split()
                    for word in title_words:
                        if similar_words.__contains__(word.lower()):
                            exceptions = ['and', 'the', 'of', 'my', 'a', 'to', 'have', 'i', 'in']
                            if not exceptions.__contains__(word.lower()):
                                counter += 1
                                if counter > len(title_words) / 2 or counter > 4:
                                    messages.error(request, f"There is already an active {context['type'].lower()} report in {context['location']} that is similar in title to yours.", extra_tags='form_error')
                                    return render(request, "report.html", context)
            if request.user.is_authenticated:
                current_user = UserProfile.objects.get(user=request.user)
            else:
                current_user = None
            report = Report.objects.create(
                report_comment=context['comment'],
                report_title=context['title'],
                report_location=context['location'],
                report_user=current_user,
                report_type=context['type'],
                is_public=context['is_public'],
                public_description=context['public_description'],
                public_files=context['public_files']
            )

            for file in request.FILES.getlist('files'):
                if request.user.is_authenticated:
                    FileUpload.objects.create(data=file, uploader=request.user, report=report)
                else:
                    FileUpload.objects.create(data=file, report=report)
            return HttpResponseRedirect(reverse("submitted"))
        return render(request, "report.html", context)

    return render(request, "report.html", context)


@login_required
def upvote_report(request, report_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    report = get_object_or_404(Report, id=report_id)
    if request.user in report.upvoters.all():
        report.upvotes -= 1
        report.upvoters.remove(request.user)
    else:
        report.upvotes += 1
        report.upvoters.add(request.user)

    report.save()
    return JsonResponse({'upvotes': report.upvotes, 'upvoted': request.user in report.upvoters.all()})


@login_required
def delete_report(request, report_id):
    if request.method == 'POST':
        try:
            report = Report.objects.get(id=report_id, report_user=request.user.userprofile)
        except Report.DoesNotExist:
            return JsonResponse({'error': 'A user may only delete their own reports'}, status=403)
        report.delete()
        return JsonResponse({'deleted': True})

    return JsonResponse({'deleted': False, 'error': 'Invalid request'}, status=400)
    # if request.method == 'POST':
    #     report = get_object_or_404(Report, id=report_id, report_user=request.user.userprofile)
    #     # report = get_object_or_404(Report, id=report_id)  # Only for site admins to delete reports for cleanup,
    #     # # not for production
    #     try:
    #         report.delete()
    #         return JsonResponse({'deleted': True})
    #     except Exception as e:
    #         return JsonResponse({'deleted': False, 'error': 'Forbidden'}, status=403)
    # else:
    #     return JsonResponse({'deleted': False, 'error': 'Invalid request'}, status=400)
