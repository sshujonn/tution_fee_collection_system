"""tution_fee_collection_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import profile

from django.contrib import admin
from django.urls import path
from users.views import log_in, dashboard, log_out, sign_up, change_password, class_setup, section_setup, shift_setup, \
    view_structure, user_profile, fee_structure, add_fee_category, add_class

from classes import views as class_views
from institutions import views as ins_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', log_in, name='login'),
    path('signup', sign_up, name='signup'),
    path('logout', log_out, name='logout'),
    path('', dashboard, name='dashboard'),
    path('change_password/', change_password, name='change_password'),
    path('class_setup/', class_setup, name='class_setup'),
    path('section_setup/', section_setup, name='section_setup'),
    path('shift_setup/', shift_setup, name='shift_setup'),
    path('view_structure/', view_structure, name='view_structure'),
    path('user_profile/', user_profile, name='user_profile'),
    path('fee_structure/', fee_structure, name='fee_structure'),
    path('add_fee_category/', add_fee_category, name='add_fee_category'),
    path('add_class/', add_class, name='add_class'),

    # For class
    path('view_class/', class_views.StudentClassList.as_view(), name='view_studentclass'),
    path('add_studentclass/', class_views.StudentClassCreate.as_view(), name='create_studentclass'),
    path('update_class/<int:pk>/<slug:action>', class_views.StudentClasssEdit.as_view(), name='update_studentclass'),

    # For institution
    path('view_institution/', ins_views.InstitutionList.as_view(), name='view_institution'),
    path('add_institution/', ins_views.InstitutionCreate.as_view(), name='create_institution'),
    path('update_institution/<int:pk>/<slug:action>', ins_views.InstitutionEdit.as_view(), name='update_institution'),

]
