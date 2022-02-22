from django.shortcuts import render
from rest_framework.views import APIView
from finalapp.permission import UserMAnageAuthPermission

from finalapp.serializers import AdminSerializer, EmailotpverifySerializer, LoginSerializer, MobileSerializer, MobileotpverifySerializer, ProfileSerializer, RegistrationSerializer, UserManageSerializer
from.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from .utilities import *
from datetime import datetime
from django.contrib.auth import authenticate,login as auth_login ,logout as auth_logout
from django.core.mail import send_mail
from django.conf import settings



class register(APIView):
    def post(self,request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(email=serializer.data['email'])
            
            otp=random_otp(4)
            time = datetime.now()
            current_time = time.replace(tzinfo=utc)
            user.otp_expiry_time = exp_time(current_time)
            user.emailOtp = otp
            if user:
                if user.is_twofactor==True:

                 
                    subject = 'welcome to E-Grocery Store'
                    message = f'Hi {user.username}, thank you for registering in E-Grocery Store.Your OTP is {user.emailOtp}.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    user.save() 

            token_pair = TokenObtainPairSerializer()
            refresh = token_pair.get_token(user)
            access = refresh.access_token

            respose_data = {"code":CREATED,
                            "data":data,
                            "access_token":str(access),
                            "refresh":str(refresh)
                            }

            return Response(respose_data,status=CREATED)
        else:
           return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)
       
       
       
class EmailResendOtp(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        user=request.user
        print(user)
        time = datetime.now()
        current_time = time.replace(tzinfo=utc)

        if current_time > user.otp_expiry_time:
            otp=random_otp(4)
            print(otp)
            user.otp_expiry_time =exp_time(current_time)
            user.emailOtp = otp
            user.save()
            
    
            
            
            # Send Mail
            subject = 'welcome to E-Grocery Store'
            message = f'Hi {user.username},your otp is {user.emailOtp}.'
            email_from = "settings.EMAIL_HOST_USER"
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            
            ## Send SMS ##
            # message = client.messages.create(
            #                             body=f'Hi {user.email} your OTP is{user.code}. Thank You.',
            #                             from_=settings.TWILIO_PHONE_NUMBER,
            #                             to=user.country_code+user.phone_number)
       
       
            return Response(success("OTP Generated."),status=CREATED)
        else:
            return Response(fail( "Try again."),status=BAD_REQUEST)
          
       
       
class EmailOtpVerify(APIView):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        user = request.user
        print(user)
        data = request.data
        emailOtp = data['emailOtp']
        time = datetime.now()
        current_time = time.replace(tzinfo=utc)
        serializer=EmailotpverifySerializer(data=data,context={'user':user})
        if serializer.is_valid():
            if current_time < user.otp_expiry_time:
                if int(emailOtp) == user.emailOtp:
                    user.emailVerify = True
                    user.emailOtp = None
                    user.save()
            
                        
                    subject = 'welcome to E-Grocery Store'
                    message = f'Hi {user.username}, thank you for registering in E-Grocery Store your OTP is verify.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    user.save() 
                    return Response(success_data("OTP varified",data),status=OK)
                else:
                    return Response(data_fail("Invalid OTP",data),status=BAD_REQUEST)
            else:
                return Response(fail("Otp expired"),status=BAD_REQUEST)
        else:
            return Response(validationfail(serializer.errors),status=BAD_REQUEST)


class MobileNoAdd(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        user = request.user
        print(user)
        data = request.data
        serializer = MobileSerializer(user,data=data)
        if serializer.is_valid():
            if user.emailVerify==True:
                if user.mobile_number == data['mobile_number']:
                    return Response(fail("Mobile number aleady exist"),status=BAD_REQUEST)

                serializer.save()
                otp=random_otp(4)
                time = datetime.now()
                current_time = time.replace(tzinfo=utc)
                user.otp_expiry_time = exp_time(current_time)
                user.mobileOtp = otp
                user.save()
 
             
                message = client.messages.create(
                                            body=f'Hi {user.email} your OTP is{user.mobileOtp}. Thank You.',
                                            from_=settings.TWILIO_PHONE_NUMBER,
                                            to=user.country_code+user.mobile_number)
                print(message)
                return Response(success("Mobile Number Added"),status=OK)
            else:
                return Response(fail("Email is not verified"),status=BAD_REQUEST)
        else:
            return Response(validationfail(serializer.errors),status=BAD_REQUEST)
        
        
class MobileResendOtp(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        user=request.user
        print(user)
        time = datetime.now()
        current_time = time.replace(tzinfo=utc)

        if current_time > user.otp_expiry_time:
            otp=random_otp(4)
            print(otp)
            user.otp_expiry_time =exp_time(current_time)
            user.mobileOtp = otp
            user.save()
            
    
    
            
            ## Send SMS ##
            message = client.messages.create(
                                        body=f'Hi {user.email} your OTP is{user.mobileOtp}. Thank You.',
                                        from_=settings.TWILIO_PHONE_NUMBER,
                                        to=user.country_code+user.mobile_number)
            print(message)
       
       
            return Response(success("OTP Generated."),status=CREATED)
        else:
            return Response(fail( "Try again."),status=BAD_REQUEST)
          
       
        
        
class MobileOtpVerify(APIView):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        user = request.user
        print(user)
        data = request.data
        mobileOtp = data['mobileOtp']
        time = datetime.now()
        current_time = time.replace(tzinfo=utc)
        serializer=MobileotpverifySerializer(data=data,context={'user':user})
        if serializer.is_valid():
            if current_time < user.otp_expiry_time:
                if int(mobileOtp) == user.mobileOtp:
                    user.mobileVerify = True
                    user.mobileOtp = None
                    user.save()
                   
                    message = client.messages.create(
                                        body=f'Hi {user.email} your OTP is verify. Thank You.',
                                        from_=settings.TWILIO_PHONE_NUMBER,
                                        to=user.country_code+user.mobile_number
                              )
                    print(message)
                    user.save() 
                    return Response(success_data("OTP varified",data),status=OK)
                else:
                    return Response(data_fail("Invalid OTP",data),status=BAD_REQUEST)
            else:
                return Response(fail("Otp expired"),status=BAD_REQUEST)
        else:
            return Response(validationfail(serializer.errors),status=BAD_REQUEST)        
        

        
        
        

                         
                                                
class login(APIView):
    def post(self,request):
        data =request.data
        serializer=LoginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            print(user)
            if user:
                token_pair = TokenObtainPairSerializer()
                refresh = token_pair.get_token(user)
                access = refresh.access_token
                if user.is_twofactor==True:
                    otp=random_otp(4)
                    time = datetime.now()
                    current_time = time.replace(tzinfo=utc)
                    user.otp_expiry_time = exp_time(current_time)
                    user.mobileOtp = otp
                    user.emailOtp = otp
                    user.save()
                    
                    message = client.messages.create(
                                            body=f'Hi {user.email} your OTP is{user.mobileOtp}. Thank You.',
                                            from_=settings.TWILIO_PHONE_NUMBER,
                                            to=user.country_code+user.mobile_number)
                    print(message)
                    
                    subject = 'welcome to E-Grocery Store'
                    message = f'Hi {user.username}, thank you for registering in E-Grocery Store.Your OTP is {user.emailOtp}.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                else:
                    otp=random_otp(4)
                    time = datetime.now()
                    current_time = time.replace(tzinfo=utc)
                    user.otp_expiry_time = exp_time(current_time)
                    user.emailOtp = otp
                    user.save()
                    
                    subject = 'welcome to E-Grocery Store'
                    message = f'Hi {user.username}, thank you for registering in E-Grocery Store.Your OTP is {user.emailOtp}.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    
                auth_login(request,user)
                data = serializer.data
                respose_data = {"code":OK,
                                "access_token":str(access),
                                "refresh":str(refresh),
                                "data":data,    
                                "message":"Login SuccessFull!!",
                                }
                return Response(respose_data,OK)
            else:
                return Response(fail("Invalid User"),status=BAD_REQUEST)
        else:
            return Response(validationfail(serializer.errors),status=BAD_REQUEST)
        
        
        
class loginOtpVerify(APIView):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        user = request.user
        data = request.data
        emailOtp = data['emailOtp']
        time = datetime.now()
        current_time = time.replace(tzinfo=utc)
        serializer=EmailotpverifySerializer(data=data,context={'user':user})
        if serializer.is_valid():
            if current_time < user.otp_expiry_time:
                if int(emailOtp) == user.emailOtp:
                    user.emailVerify = True
                    user.loginVerify= True   
                    user.save()
                   
                    subject = 'welcome to E-Grocery Store'
                    message = f'Hi {user.username}, thank you for registering in E-Grocery Store your OTP is verify.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    
                    send_mail( subject, message, email_from, recipient_list )
                    user.save() 
                    return Response(success_data("OTP varified",data),status=OK)
              
                else:
                    return Response(data_fail("Invalid OTP",data),status=BAD_REQUEST)
            else:
                return Response(fail("Otp expired"),status=BAD_REQUEST)
        else:
            return Response(validationfail(serializer.errors),status=BAD_REQUEST)

        
        
        
class Profilecreate(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = User.objects.get(id=request.user.id)
        serializer = ProfileSerializer(user)
        data=serializer.data
        return Response(success_data("Done",data),status=OK)
    
    def patch(self,request):
        user = request.user
        data=request.data
        if user:
            if user.loginVerify==True:
                serializer = ProfileSerializer(user,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data=serializer.data
                    return Response(success_data("Done",data),status=OK)
                else:
                    return Response(validationfail(serializer.errors),status=BAD_REQUEST)
            return Response(fail("verification is not done"),status=BAD_REQUEST)
        else:
            return Response(fail("Data Invalid"),status=BAD_REQUEST)
        

    
        
        

        
class logout(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        auth_logout(request)
        return Response(success('Sucessfully logged out'),status=CREATED)



class Admin_register(APIView):

    def post(self, request):
        data=request.data
        serializer = AdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            token_pair = TokenObtainPairSerializer()
            refresh = token_pair.get_token(user)
            access = refresh.access_token

            respose_data = {"code":CREATED,
                            "data":data,
                            "access_token":str(access),
                            "refresh":str(refresh)
                            }
            return Response(respose_data,status=CREATED)
        else:
            return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)
        
        
class AdminViewuser(APIView):   
    permission_classes = [IsAuthenticated,UserMAnageAuthPermission]
    def get(self, request):
        pro = User.objects.all()
        serializer = UserManageSerializer(pro, many=True)
        return Response(serializer.data)
        
        
        
        
        
        

     
       
     
class logincheck(APIView):
    permission_classes = [IsAuthenticated,UserMAnageAuthPermission]
    def get(self,request):
        if request.user.loginVerify:
             message = (f"{request.user.email}")
             return Response(success(message),status=CREATED)
        else:
            message="User is not logged in "
            return Response(fail(message),status=BAD_REQUEST)