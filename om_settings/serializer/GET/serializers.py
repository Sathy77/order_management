from rest_framework import serializers
from om_settings import models

class Settingserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings
        fields = ['id', 'company_name', 'logo', 'address', 'phone_number', 'email', 
                'vat_no', 'business_identification_number','bsti_registration_number', 'iso_certification_number',
                'website_url', 'facebook_url', 'instagram_url', 'whatsapp_url', 'tiktok_url', 'x_url', 'youtube_url']

