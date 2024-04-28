from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Report, UserProfile


class BaseTestCase(TestCase):
    def create_user_and_profile(self, username, password, is_site_admin=False):
        user = User.objects.create_user(username=username, password=password)
        profile, created = UserProfile.objects.get_or_create(user=user, defaults={'is_site_admin': is_site_admin})
        if not created:
            profile.is_site_admin = is_site_admin
            profile.save()
        return user, profile

class ReportDetailViewTests(BaseTestCase):
    def setUp(self):
        self.user, self.profile = self.create_user_and_profile('user', 'testpass', True)
        self.report = Report.objects.create(report_title="Test Report", report_user=self.profile)

    def test_report_detail_view_auth(self):
        self.client.login(username='user', password='testpass')
        response = self.client.get(reverse('report_detail', args=[self.report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Report')

    def test_report_detail_view_no_auth(self):
        response = self.client.get(reverse('report_detail', args=[self.report.id]))
        self.assertEqual(response.status_code, 302)


class DeleteReportTests(BaseTestCase):
    def setUp(self):
        self.user, self.profile = self.create_user_and_profile('user', 'testpass')
        self.other_user, self.other_profile = self.create_user_and_profile('other', 'testpass')
        self.admin_user, self.admin_profile = self.create_user_and_profile('admin', 'testpass', True)
        self.report = Report.objects.create(report_title="Test Report", report_user=self.profile)

    def test_delete_report_by_owner(self):
        self.client.login(username='user', password='testpass')
        response = self.client.post(reverse('delete_report', args=[self.report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'deleted': True})

    def test_delete_report_by_non_owner(self):
        self.client.login(username='other', password='testpass')
        response = self.client.post(reverse('delete_report', args=[self.report.id]))
        self.assertEqual(response.status_code, 403)

    def test_delete_report_by_admin(self):
        self.client.login(username='admin', password='testpass')
        response = self.client.post(reverse('delete_report', args=[self.report.id]))
        self.assertEqual(response.status_code, 403)  # Admins should not be able to delete any reports


class SubmitViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user, self.profile = self.create_user_and_profile('user', 'testpass')

    def test_submit_report_success(self):
        self.client.login(username='user', password='testpass')
        response = self.client.post(reverse('submit'), {
            'location': 'lobby',
            'type': 'noise',
            'title': 'Loud noise at night',
            'comment': 'It is very loud after 10 PM.',
            'is_public': True
        }, HTTP_REFERER='/wherever/')
        self.assertEqual(response.status_code, 302)  # Expecting redirect to "submitted" page

    def test_submit_report_failure(self):
        self.client.login(username='user', password='testpass')
        response = self.client.post(reverse('submit'), {
            'location': '',
            'type': 'noise',
            'title': '',
            'comment': 'Incomplete form submission.'
        }, HTTP_REFERER='/wherever/')
        self.assertEqual(response.status_code, 200)

    def test_submit_report_unauthenticated(self):
        response = self.client.post(reverse('submit'), {
            'location': 'lobby',
            'type': 'noise',
            'title': 'Unauthenticated report',
            'comment': 'Should not be processed.'
        }, HTTP_REFERER='/wherever/')
        self.assertEqual(response.status_code, 302)  # Expecting redirect to login page


class UpvoteReportTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user, self.profile = self.create_user_and_profile('user', 'testpass')
        self.report = Report.objects.create(report_title="Upvotable Report", report_user=self.profile, is_public=True)

    def test_upvote_report_authenticated(self):
        self.client.login(username='user', password='testpass')
        response = self.client.post(reverse('upvote_report', args=[self.report.id]))
        self.assertEqual(response.status_code, 200)
        updated_report = Report.objects.get(id=self.report.id)
        self.assertEqual(updated_report.upvotes, 1)

    def test_upvote_report_unauthenticated(self):
        response = self.client.post(reverse('upvote_report', args=[self.report.id]))
        self.assertEqual(response.status_code, 302)  # Redirected to log in since user is not authenticated


class UpdateResolutionTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.admin_user, self.admin_profile = self.create_user_and_profile('admin', 'testpass', True)
        self.user, self.profile = self.create_user_and_profile('user', 'testpass', False)
        self.report = Report.objects.create(report_title="Report to Update", report_user=self.profile)

    def test_update_resolution_by_admin(self):
        self.client.login(username='admin', password='testpass')
        response = self.client.post(reverse('update_resolution', args=[self.report.id]), {
            'report_response': 'Resolution updated.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update

    def test_update_resolution_by_non_admin(self):
        self.client.login(username='user', password='testpass')
        response = self.client.post(reverse('update_resolution', args=[self.report.id]), {
            'report_response': 'Attempt to update resolution.'
        })
        self.assertEqual(response.status_code, 403)  # Forbidden


class UserProfileTests(BaseTestCase):
    def test_user_profile_creation(self):
        user, profile = self.create_user_and_profile('testuser', 'password123', is_site_admin=True)
        self.assertTrue(isinstance(profile, UserProfile))
        self.assertEqual(profile.user.username, 'testuser')
        self.assertTrue(profile.is_site_admin)

    def test_user_profile_default_admin_status(self):
        user, profile = self.create_user_and_profile('newuser', 'password123')
        self.assertFalse(profile.is_site_admin)


class ReportTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user, self.profile = self.create_user_and_profile('reportuser', 'password')

    def test_report_creation(self):
        report = Report.objects.create(
            report_title="Noise Complaint",
            report_comment="There is a lot of noise every night after 10 PM.",
            report_location="Balz-Dobie",
            report_type=Report.NOISE,
            report_user=self.profile
        )
        self.assertTrue(isinstance(report, Report))
        self.assertEqual(report.report_user.user.username, 'reportuser')
        self.assertEqual(report.report_status, Report.NEW)
        self.assertFalse(report.is_public)

    def test_report_string_representation(self):
        report = Report.objects.create(
            report_title="Maintenance Needed",
            report_comment="Elevator is broken.",
            report_location="Gibbons",
            report_type=Report.MAINTENANCE,
            report_user=self.profile
        )
        self.assertEqual(str(report), "Maintenance Needed")
