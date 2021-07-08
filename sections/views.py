from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sections.models import sections
from classes.models import StudentClass
from branches.models import Branch
from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService

gs = GlobalService()


# Create your views here.

class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        branch = Branch.objects.filter(branch_admins=request.user)[0]
        queryset = StudentClass.objects.filter(branch=branch)
        if not request or not queryset:
            return None
        return queryset.filter(branch=branch)

class SectionSerializer(serializers.ModelSerializer):
    student_class = UserFilteredPrimaryKeyRelatedField()
    class Meta:
        model = sections
        fields = (
            'id',
            'section_name',
            'section_shift',
            'student_class',
        )


class SectionFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = sections
        fields = '__all__'


class SectionList(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Sections/view_sections.html'
    # template_name = 'dashboard/dashboard.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        branch = Branch.objects.filter(branch_admins=request.user)[0]

        # import pdb;pdb.set_trace()
        items = sections.objects.filter(student_class__in=StudentClass.objects.filter(branch = branch))
        items = c_serializers.serialize("python", items)

        return Response({'serializer': items, 'menu': menu}, template_name=self.template_name)


class SectionCreate(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Sections/create_section_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = SectionSerializer(context={'request': request})
        return Response({'serializer': serializer, 'menu': menu}, template_name=self.template_name)

    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data, {'created_by': request.user.id})
        # modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = SectionFieldsSerializer(context=request, data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_sections'))


class SectionEdit(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Sections/edit_section_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, pk, action=None):
        item = sections.objects.filter()

        menu = gs.get_menu(request.user)

        if len(item) < 1:
            messages.warning(request, 'Only creator of this project can update')
            return HttpResponseRedirect(reverse('view_sections'))
        item = item.get(pk=pk)
        if action == 'delete':
            item.delete()
        else:
            serializer = SectionSerializer(item, context={'request': request})
            return Response({'serializer': serializer, 'item': item, 'menu': menu}, template_name=self.template_name)

        return HttpResponseRedirect(reverse('view_sections'))

    def post(self, request, pk, action):
        item = sections.objects.filter().get(pk=pk)
        serializer = SectionSerializer(item, data=request.data)

        if action == 'update':
            if serializer.is_valid():
                serializer.save()

        return HttpResponseRedirect(reverse('view_sections'))
