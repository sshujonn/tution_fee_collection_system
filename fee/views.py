from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fee.models import Fee
from branches.models import Branch
from classes.models import StudentClass
from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService

gs = GlobalService()


# Create your views here.
class FeeSerializer(serializers.ModelSerializer):
    student_class = serializers.SerializerMethodField('_is_my_find')

    def _is_my_find(self, obj):
        user_id = self.context.get("user_id")
        if user_id:
            branch = Branch.objects.filter(branch_admins=request.user)[0]
            # import pdb;pdb.set_trace()
            classes = StudentClass.objects.filter(branch=branch)
            print (classes)
            return classes
            # return user_id in obj.my_objects.values_list("user_id", flat=True)
        return False

    # student_class = serializers.PrimaryKeyRelatedField(queryset=StudentClass.objects.filter())
    # student_class = is_my_object
    class Meta:
        model = Fee
        fields = (
            'id',
            'fee_name',
            'fee_amount',
            'student_class',
        )


class FeeFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'


class FeeList(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Fees/view_fees.html'
    # template_name = 'dashboard/dashboard.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        branch = Branch.objects.filter(branch_admins=request.user)[0]


        items = Fee.objects.filter(student_class__in=StudentClass.objects.filter(branch = branch))
        items = c_serializers.serialize("python", items)

        return Response({'serializer': items, 'menu': menu}, template_name=self.template_name)




class FeeCreate(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Fees/create_fee_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = FeeSerializer(context={'user_id': request.user.id})
        return Response({'serializer': serializer, 'menu': menu}, template_name=self.template_name)

    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data, {'created_by': request.user.id})
        # modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = FeeFieldsSerializer(context=request, data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_fee'))


class FeeEdit(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/Fees/edit_fee_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, pk, action=None):
        item = Fee.objects.filter()

        menu = gs.get_menu(request.user)

        if len(item) < 1:
            messages.warning(request, 'Only creator of this project can update')
            return HttpResponseRedirect(reverse('view_fee'))
        item = item.get(pk=pk)
        if action == 'delete':
            item.delete()
        else:
            serializer = FeeSerializer(item)
            return Response({'serializer': serializer, 'item': item, 'menu': menu}, template_name=self.template_name)

        return HttpResponseRedirect(reverse('view_fee'))

    def post(self, request, pk, action):
        item = Fee.objects.filter().get(pk=pk)
        serializer = FeeSerializer(item, data=request.data)

        if action == 'update':
            if serializer.is_valid():
                serializer.save()

        return HttpResponseRedirect(reverse('view_fee'))


