import profile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone



class UserManager(BaseUserManager):
    def _create_user(self, email, password,is_staff,is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            createdAt=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password,False,False,**extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password,True,True,**extra_fields)
        user.save(using=self._db)
        return user




class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)
    country_code=models.CharField(max_length=4,null=True)
    
    firstname=models.CharField(max_length=100,null=True)
    lastname=models.CharField(max_length=100,null=True,)
    age=models.IntegerField(null=True) 
    address = models.TextField(null=True)
    age = models.CharField(max_length=3)
    profile_image = models.ImageField(null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    profession  = models.CharField(max_length=100)
    hobbies = models.CharField(max_length=100)
    
    emailOtp = models.IntegerField(null=True)
    mobileOtp = models.IntegerField(null=True)
    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    
    otp_expiry_time = models.DateTimeField(null=True)
    
    emailVerify = models.BooleanField(default=False)
    mobileVerify =  models.BooleanField(default=False)
    loginVerify = models.BooleanField(default=False)

    is_twofactor = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    

    
    def __str__(self):
        return self.email
    
    
