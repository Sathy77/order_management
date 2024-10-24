from django.db import models
from helps.abstract.abstractclass import Basic
from helps.common.generic import Generichelps as ghelp

# Create your models here.
def generate_unique_code():
    return ghelp().getUniqueCodePattern()

def uploadcompanylogo(instance, filename):
    return "files/company/{name}/logo/{uniquecode}uniquevalue{filename}".format(name=instance.company_name, uniquecode=generate_unique_code(), filename=filename)

class Settings(Basic):
    company_name = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to=uploadcompanylogo, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    vat_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    business_identification_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    bsti_registration_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    iso_certification_number = models.CharField(max_length=50, unique=True, blank=True, null=True)

    website_url = models.URLField(max_length=200, unique=True, blank=True, null=True)
    facebook_url = models.URLField(max_length=200, unique=True, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, unique=True, blank=True, null=True)
    whatsapp_url = models.URLField(max_length=200, unique=True, blank=True, null=True)
    tiktok_url = models.URLField(max_length=200, unique=True, blank=True, null=True)
    x_url = models.URLField(max_length=200, unique=True, blank=True, null=True)
    youtube_url = models.URLField(max_length=200, unique=True, blank=True, null=True)
    
    def __str__(self):
        return f'{self.id} - {self.company_name}' 