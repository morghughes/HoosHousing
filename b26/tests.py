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
