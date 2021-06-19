from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from students.models import students
from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService

gs = GlobalService()


# Create your views here.
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = students
        fields = (
            'id',
            'student_name',
            'student_gender',
            'student_dob',
            'student_address',
            'student_religion',
            'student_father_name',
            'student_mother_name',
            'session_start_date',
            'session_end_date',
        )


class StudentFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = students
        fields = '__all__'


class StudentList(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Students/view_students.html'
    # template_name = 'dashboard/dashboard.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)

        items = students.objects.all()
        items = c_serializers.serialize("python", items)

        return Response({'serializer': items, 'menu': menu}, template_name=self.template_name)


class StudentCreate(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Students/create_student_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = StudentSerializer()
        return Response({'serializer': serializer, 'menu': menu}, template_name=self.template_name)

    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data, {'created_by': request.user.id})
        # modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = StudentFieldsSerializer(context=request, data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_students'))


class StudentEdit(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Students/edit_student_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, pk, action=None):
        item = students.objects.filter()

        menu = gs.get_menu(request.user)

        if (len(item) < 1):
            messages.warning(request, 'Only creator of this project can update')
            return HttpResponseRedirect(reverse('view_students'))
        item = item.get(pk=pk)
        if action == 'delete':
            item.delete()
        else:
            serializer = StudentSerializer(item)
            return Response({'serializer': serializer, 'item': item, 'menu': menu}, template_name=self.template_name)

        return HttpResponseRedirect(reverse('view_students'))

    def post(self, request, pk, action):
        item = students.objects.filter().get(pk=pk)
        serializer = StudentSerializer(item, data=request.data)

        if action == 'update':
            if serializer.is_valid():
                serializer.save()

        return HttpResponseRedirect(reverse('view_students'))
