from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from institutions.models import Institution
from students.models import students
from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService

gs = GlobalService()
# Create your views here.
class PaymentPage(APIView):
    permission_classes = (AllowAny,)
    template_name = 'dashboard/payment/payment.html'
    renderer_classes = [renderers.TemplateHTMLRenderer,]

    def get(self, request):
        items = Institution.objects.all()
        items = c_serializers.serialize("python", items)

        # return Response({'serializer': items})
        return Response({'serializer': items}, template_name=self.template_name)

class ValidatePayment(APIView):
    permission_classes = (AllowAny,)
    template_name = 'dashboard/payment/payment.html'
    renderer_classes = [renderers.JSONRenderer,]

    def get(self, request):
        items = Institution.objects.all()
        items = c_serializers.serialize("python", items)

        # return Response({'serializer': items})
        return Response({'serializer': items})