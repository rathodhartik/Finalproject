
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication



    
class UserMAnageAuthPermission(BasePermission):
     ADMIN_ONLY_AUTH_CLASSES=[BaseAuthentication,]
    
     def has_permission(self, request, view):
        user=request.user
        if user and user.is_authenticated and user.is_staff:
           return user or \
              not any(isinstance(request._authenticator ,x)for x in self.ADMIN_ONLY_AUTH_CLASSES)
        return False
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#from django.contrib.auth.models import Permission,Group
# from groceryapp.models import User
# from rest_framework.response import Response
# from rest_framework import permissions,status
# from functools import wraps
# from django.contrib.auth.decorators import login_required,user_passes_test
