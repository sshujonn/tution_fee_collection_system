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
from branches import views as branch_views
from fee import views as fee_views
from sections import views as section_views
from student_category import views as student_category_views
from students import views as students_views

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

    # For branch
    path('view_branch/', branch_views.BranchList.as_view(), name='view_branch'),
    path('add_branch/', branch_views.BranchCreate.as_view(), name='create_branch'),
    path('update_branch/<int:pk>/<slug:action>', branch_views.BrachEdit.as_view(), name='update_branch'),

    # For fee
    path('view_fee/', fee_views.FeeList.as_view(), name='view_fee'),
    path('add_fee/', fee_views.FeeCreate.as_view(), name='create_fee'),
    path('update_fee/<int:pk>/<slug:action>', fee_views.FeeEdit.as_view(), name='update_fee'),

    # For Sections
    path('view_section/', section_views.SectionList.as_view(), name='view_sections'),
    path('add_section/', section_views.SectionCreate.as_view(), name='create_sections'),
    path('update_section/<int:pk>/<slug:action>', section_views.SectionEdit.as_view(), name='update_sections'),

    # For Student Category
    path('view_student_category/', student_category_views.StudentCategoryList.as_view(), name='view_studentcategory'),
    path('add_student_category/', student_category_views.StudentCategoryCreate.as_view(), name='create_studentcategory'),
    path('update_student_category/<int:pk>/<slug:action>', student_category_views.StudentCategoryEdit.as_view(), name='update_studentcategory'),

    # For Student Category
    path('view_students/',  students_views.StudentList.as_view(), name='view_students'),
    path('add_students/', students_views.StudentCreate.as_view(), name='create_students'),
    path('update_students/<int:pk>/<slug:action>', students_views.StudentEdit.as_view(), name='update_students'),
]
