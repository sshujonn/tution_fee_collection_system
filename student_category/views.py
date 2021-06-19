from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from student_category.models import student_category
from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService

gs = GlobalService()


# Create your views here.
class StudentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = student_category
        fields = (
            'id',
            'student_category_name',
        )


class StudentCategoryFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = student_category
        fields = '__all__'


class StudentCategoryList(APIView):
    permission_classes = (IsAuthenticated,)
    template_name = 'dashboard/Student_Categories/view_student_categories.html'
    # template_name = 'dashboard/dashboard.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)

        items = student_category.objects.all()
        items = c_serializers.serialize("python", items)

        return Response({'serializer': items, 'menu': menu}, template_name=self.template_name)


class StudentCategoryCreate(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Student_Categories/create_student_category_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]


    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = StudentCategorySerializer()
        return Response({'serializer': serializer, 'menu': menu}, template_name=self.template_name)

    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data, {'created_by': request.user.id})
        # modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = StudentCategoryFieldsSerializer(context=request, data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_student_category'))
