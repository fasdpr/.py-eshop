from django.contrib.auth.mixins import UserPassesTestMixin

from kavenegar import *
def send_otp_code(phone_number,code):
    try:
        api = KavenegarAPI('3753387267726B6E79536E2B4E52785A48375566702B5152646C324644546C73764D5044666A386658354D3D')
        params = {
        'sender': '',#optional
        'receptor': '',#multiple mobile number, split by comma
        'message': f'{code}کد تایید شما',
    } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)

class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self,request):
        return self.request.user.is_authenticated and self.request.user.is_admin
