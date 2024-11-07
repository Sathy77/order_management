import requests
import json
from otp import models as MODELS_OTP


def send_otp(otp, phone):
    phone = '+'.join(phone)
    url = f'http://45.120.38.242/api/sendsms?api_key=01706462882.Ip9cP6VKuyvgPFfvwF&type=text&phone={phone}&senderid=8809604903051&message={otp}'

    payload = json.dumps({})
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=b0sQqulZsrFJYZ43GmSX4co9CkwTw5Ld; sessionid=5jlvcowmr75e3ghxf017dw0953wrqtr3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code


def verify_otp(contact_no, otp_code):
    response = {'flag': False, 'message': []}

    contact_no = '8801' + contact_no[-9:]
    print(contact_no)

    try:
        otp_instance = MODELS_OTP.Otp.objects.get(phone=contact_no, otp_code=otp_code)

        # Check if the OTP is expired
        if otp_instance.is_expired():
            response['message'].append("OTP has expired.")
        else: 
            response['flag']= True
            response['message'].append("OTP verified successfully!")
        # OTP is valid and not expired

    except MODELS_OTP.Otp.DoesNotExist:
        response['message'].append("Invalid OTP or phone number.")
        
    return response