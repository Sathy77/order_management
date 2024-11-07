from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.decorators import api_view
from otp import models as MODELS_OTP
from otp import sendotp 
from django.utils import timezone
from datetime import timedelta



@api_view(['POST'])
def generate_otp(request):
    status_code = status.HTTP_400_BAD_REQUEST
    requestdata = request.data.copy()
    contact_no = requestdata.get('contact_no')
    contact_no = '8801' + contact_no[-9:]
    otp = random.randint(1000, 9999)
    phone = [contact_no]
    # Create and save a new OTP
    otpintance = MODELS_OTP.Otp(phone=contact_no, otp_code=otp)
    print(otpintance)
    otpintance.save()

    cutoff_time = timezone.now() - timedelta(minutes=10)
    old_otps = MODELS_OTP.Otp.objects.filter(created_at__lt=cutoff_time)
    old_otps.delete()

    status_code = sendotp.send_otp(otp, phone)

    return Response( status=status_code)

# @api_view(['POST'])
# def verify_otp(request):
#     requestdata = request.data
#     contact_no = requestdata.get('contact_no')
#     otp_code = requestdata.get('otp')
#     print(requestdata)
    
#     contact_no = '8801' + contact_no[-9:]
#     print(contact_no)

#     try:
#         otp_instance = MODELS_OTP.Otp.objects.get(phone=contact_no, otp_code=otp_code)

#         # Check if the OTP is expired
#         if otp_instance.is_expired():
#             return Response({"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

#         # OTP is valid and not expired
#         return Response({"message": "OTP verified successfully!"}, status=status.HTTP_200_OK)

#     except MODELS_OTP.Otp.DoesNotExist:
#         return Response({"message": "Invalid OTP or phone number."}, status=status.HTTP_400_BAD_REQUEST)