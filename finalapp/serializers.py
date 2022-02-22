from .models import User
from rest_framework import serializers




""" User Registration"""
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password','is_twofactor')
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
""" Email OTP Verify"""
class EmailotpverifySerializer(serializers.ModelSerializer):
    emailOtp = serializers.CharField(max_length=4,min_length=4,required=True)
    class Meta:
        model=User
        fields = ('emailOtp',)
    
""" Mobile Number Add"""   
class MobileSerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(required=True,max_length=4)
    mobile_number = serializers.CharField(min_length=10,max_length=10)
    class Meta:
        model=User
        fields = ('mobile_number','country_code')
        
""" Mobile OTP Verify"""
class MobileotpverifySerializer(serializers.ModelSerializer):
    mobileOtp = serializers.CharField(max_length=4,min_length=4,required=True)
    class Meta:
        model=User
        fields = ('mobileOtp',)
        
        
""" Login """
class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email','password',)



          
""" Admin Registration"""
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        
    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)
    
    
class UserManageSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ('id','username','email', 'firstname', 'lastname','age','emailVerify','mobileVerify','loginVerify','is_active','is_staff','is_superuser')
        
        
     def update(self, instance, validated_data):
           instance.username=validated_data.get('username',instance.username)
           instance.email=validated_data.get('email',instance.email)
           instance.firstname=validated_data.get('firstname',instance.firstname)
           instance.lastname=validated_data.get('lastname',instance.lastname)
           instance.age=validated_data.get('age',instance.age)
           instance.save()
           return instance
            

""" ProfileSerializer """
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields=('firstname', 'lastname', 'age','city','state','country','profession','hobbies')
      
    def validated(self, data):
        firstname =  data.get('firstname')
        lastname = data.get('lastname')

        if firstname == lastname:
            raise serializers.ValidationError({"lastname": ["FirstName and LastName shouldn't be same."]})
    

    
    def update(self, instance, validated_data):
      instance.firstname=validated_data.get('firstname',instance.firstname)
      instance.lastname=validated_data.get('lastname',instance.lastname)
      instance.age=validated_data.get('age',instance.age)
    #   instance.profile_image=validated_data.get('profile_image',instance.profile_image)
      instance.city=validated_data.get('city',instance.city)
      instance.state=validated_data.get('state',instance.state)
      instance.country=validated_data.get('country',instance.country)
      instance.profession=validated_data.get('profession',instance.profession)
      instance.hobbies=validated_data.get('hobbies',instance.hobbies)
      instance.save()
      return instance

        