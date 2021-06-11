from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from institutions.models import Institution
from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService

gs = GlobalService()


# Create your views here.

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            'id',
            'institution_name',
            'institution_address',
            'institution_phone_number',
        )


class InstitutionFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionList(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Institutions/view_institutions.html'
    # template_name = 'dashboard/dashboard.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)

        items = Institution.objects.all()
        items = c_serializers.serialize("python", items)

        return Response({'serializer': items, 'menu': menu}, template_name=self.template_name)

class InstitutionCreate(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Institutions/create_institution_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = InstitutionSerializer()
        return Response({'serializer': serializer, 'menu': menu}, template_name=self.template_name)

    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data, {})
        # modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = InstitutionFieldsSerializer(context=request, data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_institution'))


class InstitutionEdit(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Institutions/edit_institution_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, pk, action=None):
        item = Institution.objects.filter()
        menu = gs.get_menu(request.user)

        if (len(item) < 1):
            messages.warning(request, 'Only creator of this item can update')
            return HttpResponseRedirect(reverse('view_institution'))
        item = item.get(pk=pk)
        if action == 'delete':
            item.delete()
        else:
            serializer = InstitutionSerializer(item)
            return Response({'serializer': serializer, 'item': item, 'menu': menu}, template_name=self.template_name)

        return HttpResponseRedirect(reverse('view_institution'))

    def post(self, request, pk, action):
        item = Institution.objects.filter().get(pk=pk)
        serializer = InstitutionSerializer(item, data=request.data)

        if action == 'update':
            if serializer.is_valid():
                serializer.save()

        return HttpResponseRedirect(reverse('view_institution'))