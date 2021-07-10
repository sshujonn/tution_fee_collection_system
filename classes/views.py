from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from classes.models import StudentClass
from branches.models import Branch
from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService

gs = GlobalService()


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = (
            'id',
            'class_name',
            'branch',
        )


class StudentClassFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = '__all__'


class StudentClassCreate(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Classes/create_classes_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = StudentClassSerializer()
        return Response({'serializer': serializer, 'menu': menu}, template_name=self.template_name)

    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data, {'created_by': request.user.id})
        # modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = StudentClassFieldsSerializer(context=request, data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_studentclass'))


class StudentClassList(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Classes/view_classes.html'
    # template_name = 'dashboard/dashboard.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        if not request.user.is_superuser:
            branch = Branch.objects.filter(branch_admins = request.user)[0]
            # import pdb;pdb.set_trace()
            projects = StudentClass.objects.filter(branch = branch)
        else:
            projects = StudentClass.objects.all()
        projects = c_serializers.serialize("python", projects)

        return Response({'serializer': projects, 'menu': menu}, template_name=self.template_name)


class StudentClassListByBranch(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, branch_id):
        projects = StudentClass.objects.filter(branch_id=branch_id)
        projects = c_serializers.serialize("python", projects)
        return Response({'serializer': projects})

class StudentClasssEdit(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Classes/edit_classes_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, pk, action=None):
        item = StudentClass.objects.filter()

        menu = gs.get_menu(request.user)

        if len(item) < 1:
            messages.warning(request, 'Only creator of this project can update')
            return HttpResponseRedirect(reverse('view_studentclass'))
        item = item.get(pk=pk)
        if action == 'delete':
            item.delete()
        else:
            serializer = StudentClassSerializer(item)
            return Response({'serializer': serializer, 'item': item, 'menu': menu}, template_name=self.template_name)

        return HttpResponseRedirect(reverse('view_studentclass'))

    def post(self, request, pk, action):
        item = StudentClass.objects.filter().get(pk=pk)
        serializer = StudentClassSerializer(item, data=request.data)

        if action == 'update':
            if serializer.is_valid():
                serializer.save()

        return HttpResponseRedirect(reverse('view_studentclass'))
