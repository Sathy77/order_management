from django.db import models
from django.contrib.auth.models import AbstractUser
from helps.abstract.abstractclass import Basic
from datetime import timedelta
from helps.choice import common as CHOICE
from helps.common.generic import Generichelps as ghelp

# Create your models here.
def generate_unique_code():
    return ghelp().getUniqueCodePattern()

class Permission(Basic):
    name = models.CharField(max_length=50, unique=True)
    # code  = models.CharField(max_length=15, default=generate_code, unique=True, editable=False)
    # active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.name}'
    
class Role(Basic):
    name = models.CharField(max_length=50, blank=True, null=True)
    permission = models.ManyToManyField(Permission, blank=True)
    # active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

class User(AbstractUser):
    name = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    contact_no = models.CharField(max_length=14, unique=True, blank=True, null=True)

    role = models.ManyToManyField(Role, blank=True)

    uniqueid = models.CharField(max_length=18, unique=True, default=generate_unique_code)
    # uniqueid = models.CharField(max_length=18, unique=True)

    # designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True) # Mandatory
    ###
    user_type = models.CharField(max_length=25, choices=CHOICE.USER_TYPE , default=CHOICE.USER_TYPE[1][1])
    dob = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=25, choices=CHOICE.BLOOD_GROUP, blank=True, null=True)
    fathers_name = models.CharField(max_length=150, blank=True, null=True)
    mothers_name = models.CharField(max_length=150, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=CHOICE.MARITAL_STATUS, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=CHOICE.GENDER, blank=True, null=True)
    ###
    #####
    # religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, blank=True, null=True)
    # personal_email = models.EmailField(blank=True)
    #####
    # role_permission = models.ManyToManyField(Rolepermission, blank=True)
    # grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, blank=True, null=True)
    # shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, blank=True, null=True)
    ###
    # present_address = models.OneToOneField(MODELS_CONT.Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='userseven')
    # permanent_address = models.OneToOneField(MODELS_CONT.Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='usereight')
    # #####
    # dummy_salary = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    # joining_date = models.DateField(blank=True, null=True)
    # #######
    # allow_overtime = models.BooleanField(default=False)
    # allow_remote_checkin = models.BooleanField(default=False)
    # active_dummy_salary = models.BooleanField(default=False)
    # job_status = models.CharField(max_length=30, choices=CHOICE.JOB_STATUS, blank=True, null=True)
    # official_note = models.TextField(blank=True, null=True)
    # photo = models.ImageField(upload_to=upload_user_photo, blank=True, null=True)
    # rfid = models.CharField(max_length=50, unique=True, blank=True, null=True)
    # #########
    # hr_password = models.CharField(max_length=550, blank=True, null=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='userone')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='usertwo')
    
    def __str__(self):
        return f'{self.id} - {self.username}'
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
