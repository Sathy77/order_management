from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from helps.decorators.decorator import CommonDecorator as deco
from om_settings import models as MODELS_OMSE
from om_settings.serializer.POST import serializers as POST_SRLZER_OMSE
from om_settings.serializer.GET import serializers as GET_SRLZER_OMSE
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_nested_forms.utils import NestedForm
from rest_framework import status
from order_management.settings import BASE_DIR
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['view_setting'])
def getsettings(request):
    if not MODELS_OMSE.Settings.objects.all().exists():
        demo_logo_path=BASE_DIR / 'media/files/company/default/logo/demo.jpg'
        image = Image.open(demo_logo_path)
        thumb_io = BytesIO()
        image.save(thumb_io, format='JPEG')
        
        instance=MODELS_OMSE.Settings()
        instance.company_name='Your Company name'
        instance.address='Your Company address'
        instance.phone_number='01700000000'
        instance.email='gamil@gmail.com'
        instance.logo.save('logo.jpg', ContentFile(thumb_io.getvalue()), save=True)
        instance.save()
        
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'company_name', 'convert': None, 'replace':'company_name__icontains'},
        {'name': 'address', 'convert': None, 'replace':'address__icontains'},
        {'name': 'phone_number', 'convert': None, 'replace':'phone_number__icontains'},
        {'name': 'email', 'convert': None, 'replace':'email'},

        {'name': 'vat_no', 'convert': None, 'replace':'vat_no__icontains'},
        {'name': 'business_identification_number', 'convert': None, 'replace':'business_identification_number__icontains'},
        {'name': 'bsti_registration_number', 'convert': None, 'replace':'bsti_registration_number__icontains'},
        {'name': 'iso_certification_number', 'convert': None, 'replace':'iso_certification_number__icontains'},

        {'name': 'website_url', 'convert': None, 'replace':'website_url__icontains'},
        {'name': 'facebook_url', 'convert': None, 'replace':'facebook_url__icontains'},
        {'name': 'instagram_url', 'convert': None, 'replace':'instagram_url__icontains'},
        {'name': 'whatsapp_url', 'convert': None, 'replace':'whatsapp_url__icontains'},
        {'name': 'tiktok_url', 'convert': None, 'replace':'tiktok_url__icontains'},
        {'name': 'x_url', 'convert': None, 'replace':'x_url__icontains'},
        {'name': 'youtube_url', 'convert': None, 'replace':'youtube_url__icontains'},
    ]

    settings = MODELS_OMSE.Settings.objects.filter(**ghelp().KWARGS(request, filter_fields))
    settings, total_count, page, page_size = ghelp().getPaginatedData(request, settings)
    settingserializers = GET_SRLZER_OMSE.Settingserializer(settings, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': settingserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['get company info', 'all'])
# def addsetting(request):
#     requestdata = dict(request.data)
#     requestdata.update({'abcdef[abcdef]': ['abcdef']})
#     options = {'allow_blank': True, 'allow_empty': False}
#     form = NestedForm(requestdata, **options)
#     form.is_nested(raise_exception=True)
#     requestdata = ghelp().prepareData(form.data, 'setting')

#     required_fields = ['company_name', 'logo', 'address', 'phone_number', 'email']
#     fields_regex = [
#         {'field': 'email', 'type': 'email'},
#         {'field': 'phone_number', 'type': 'phonenumber'},
#     ]
#     response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
#         classOBJ=MODELS_OMSE.Settings, 
#         Serializer=POST_SRLZER_OMSE.Settingserializer, 
#         data=requestdata, 
#         unique_fields=[], 
#         fields_regex=fields_regex, 
#         required_fields=required_fields
#     )
#     if response_data: response_data = response_data.data
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['edit_setting'])
def updatesetting(request, settingid=None):
    requestdata = dict(request.data)
    requestdata.update({'abcdef[abcdef]': ['abcdef']})
    options = {'allow_blank': True, 'allow_empty': False}
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)
    requestdata = ghelp().prepareData(form.data, 'setting')
    allowed_fields=['company_name', 
                    'logo', 
                    'address', 
                    'phone_number', 
                    'email', 
                    'vat_no', 
                    'business_identification_number',
                    'bsti_registration_number', 
                    'iso_certification_number',
                    'website_url', 
                    'facebook_url', 
                    'instagram_url', 
                    'whatsapp_url', 
                    'tiktok_url', 
                    'x_url', 
                    'youtube_url']
    
    static_fields = ['logo']
    fields_regex = [
        {'field': 'email', 'type': 'email'},
        {'field': 'phone_number', 'type': 'phonenumber'},
    ]
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_OMSE.Settings, 
        Serializer=POST_SRLZER_OMSE.Settingserializer, 
        id=settingid, 
        data=requestdata,
        allowed_fields=allowed_fields,
        fields_regex=fields_regex,
        static_fields=static_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
