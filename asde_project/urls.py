from django.contrib import admin
from django.urls import path, include
# from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from b26 import views
from b26.views import mark_report_complete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome_view, name='welcome'),
    # path('index/', views.index, name='index'),
    #path('', views.index, name='home'),
    # path('', views.signin_view, name='signin'),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload/', views.upload_file, name='upload'),
    path('report/', views.report_view, name='report'),
    path('submitted/', views.SubmittedView.as_view(), name="submitted"),
    path('submit/', views.submit, name="submit"),
    path('view_reports/', views.view_reports, name='view_reports'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    # path('welcome/', views.welcome_view, name='welcome'),
    path('reports/<int:report_id>/mark_complete/', mark_report_complete, name='mark_complete'),
    path('reports/<int:report_id>/update_resolution/', views.update_resolution, name='update_resolution'),
    path('reports/upvote/<int:report_id>/', views.upvote_report, name='upvote_report'),
    path('reports/delete/<int:report_id>/', views.delete_report, name='delete_report'),
]
