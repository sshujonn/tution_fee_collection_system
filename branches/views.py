from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from branches.models import Branch
from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService

gs = GlobalService()


# Create your views here.
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = (
            'id',
            'branch_name',
            'branch_email',
            'branch_phone_number',
            'branch_address',
            'branch_status',
            'institution',
            'branch_admins'
        )


class BranchFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class BranchList(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Branches/view_branches.html'
    # template_name = 'dashboard/dashboard.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)

        items = Branch.objects.all()

        # import pdb;pdb.set_trace()
        items = c_serializers.serialize("python", items)

        return Response({'serializer': items, 'menu': menu}, template_name=self.template_name)

class BranchListByInstitution(APIView):
    permission_classes = (AllowAny)
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, institution_id):
        items = Branch.objects.filter(institution_id=institution_id)
        items = c_serializers.serialize("python", items)

        return Response({'serializer': items})


class BranchCreate(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Branches/create_branch_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = BranchSerializer()
        return Response({'serializer': serializer, 'menu': menu}, template_name=self.template_name)

    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data, {'created_by': request.user.id})
        # modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = BranchFieldsSerializer(context=request, data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_branch'))


class BrachEdit(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Branches/edit_branch_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, pk, action=None):
        item = Branch.objects.filter()

        menu = gs.get_menu(request.user)

        if (len(item) < 1):
            messages.warning(request, 'Only creator of this project can update')
            return HttpResponseRedirect(reverse('view_branch'))
        item = item.get(pk=pk)
        if action == 'delete':
            item.delete()
        else:
            serializer = BranchSerializer(item)
            return Response({'serializer': serializer, 'item': item, 'menu': menu}, template_name=self.template_name)

        return HttpResponseRedirect(reverse('view_branch'))

    def post(self, request, pk, action):
        item = Branch.objects.filter().get(pk=pk)
        serializer = BranchSerializer(item, data=request.data)

        if action == 'update':
            if serializer.is_valid():
                serializer.save()

        return HttpResponseRedirect(reverse('view_branch'))
