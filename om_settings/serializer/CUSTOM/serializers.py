from rest_framework import serializers
from om_settings import models

class Settingserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings
        fields = ['id', 'company_name', 'logo', 'address', 'phone_number', 'email', 
                'website_url', 'facebook_url', 'instagram_url', 'whatsapp_url', 'tiktok_url', 'x_url', 'youtube_url']


