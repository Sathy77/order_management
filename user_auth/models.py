from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from helps.common.generic import Generichelps as ghelp
from helps.abstract.abstractclass import Basic
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def reset_password_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    
    send_mail(
        #title
        "password Reset for {title}".format(title="hrm"),
        
        #message
        email_plaintext_message,
        
        #from
        'admin@admin.com',
        
        #to
        [reset_password_token.user.email]
        # ['naymhsain00@gmail.com']
    )