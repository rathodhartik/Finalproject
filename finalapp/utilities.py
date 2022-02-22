from copy import error
import math
import random
from urllib import request
from rest_framework import status

import datetime
from random import randint
from django.conf import settings

from twilio.rest import Client

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)



OK = status.HTTP_200_OK
CREATED = status.HTTP_201_CREATED
BAD_REQUEST =status.HTTP_400_BAD_REQUEST
NO_CONTENT =status.HTTP_204_NO_CONTENT
NOT_FOUND = status.HTTP_404_NOT_FOUND





def success(message):
   
    msg={"code":CREATED,
        "message":message}
    return msg





def login_success(message,data,access,refresh):
     user_data={
        "user":data,
        "access_token":access,
        "refresh_token":refresh}
     msg={"code":CREATED,"message":message,"data":user_data}
     return msg

def data_fail(message,data):
    msg={"code":BAD_REQUEST,
         "message":message,
         "data":data}
    return msg



def validationfail(data):
    fail = {"code":BAD_REQUEST,
            "data":data}
    return fail

def fail(message):
    fail = {"code":BAD_REQUEST,
            "message":message}
    return fail

def update_data(message,data):
    msg={"code":OK,
             "message":message,
             "data":data}
    return msg

def success_data(message,data):
    msg={"code":OK,
             "message":message,
             "data":data}
    return msg

def deleted_data(message):
    msg={"code":NO_CONTENT,
             "message":message,}
    return msg


def success_mount(message,data,amount,quantity):
     user_data={
        "user":data,
        "total_amount":amount,
        "total_quantity":quantity,}
     msg={"code":CREATED,"message":message,"data":user_data}
     return msg


def not_found(message):
   
    msg={"code":NOT_FOUND,
        "message":message}
    return msg





## Date time

import pytz
utc=pytz.UTC
time = datetime.datetime.now()
current_time = time.replace(tzinfo=utc)

def exp_time(now):
    expired = now+datetime.timedelta(seconds=60)
    return expired


## OTP

# def random_otp() :
 
#     digits = "0123456789"
#     OTP = ""
#     for i in range(4) :
#         OTP += digits[math.floor(random.random() * 10)]
 
#     return OTP


def random_otp(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


