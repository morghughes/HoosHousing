"""
URL configuration for asde_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from b26 import views
from b26.views import mark_report_complete

# from b26.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('accounts/', include('allauth.urls')),
    # path('accounts/login', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload/', views.upload_file, name='upload'),
    path('report/', views.report_view, name='report'),
    path('submitted/', views.SubmittedView.as_view(), name="submitted"),
    path('submit/', views.submit, name = "submit"),
    path('view_reports/', views.view_reports, name='view_reports'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('reports/<int:report_id>/mark_complete/', mark_report_complete, name='mark_complete'),
    path('reports/<int:report_id>/update_resolution/', views.update_resolution, name='update_resolution'),
    path('reports/upvote/<int:report_id>/', views.upvote_report, name='upvote_report'),
]
