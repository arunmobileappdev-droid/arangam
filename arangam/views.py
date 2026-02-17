from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import UserDetail
from .Serializer import UserDetailModelSerializer
from rest_framework.response import Response
from rest_framework import status
import secrets
import string
from .hash_function import hash_password,verify_password

@api_view(['GET'])
def get_user_list(request):
    userDetail = UserDetail.objects.all()
    serializer = UserDetailModelSerializer(userDetail,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
     
    user_id = request.data.get('user_id')
    user_name = request.data.get('user_name')
    email = request.data.get('email')
    phone = request.data.get('phone')
    age = request.data.get('age')
    password = request.data.get('password')
    
    if not all([user_id, user_name, email,phone, password, age]):
        return Response(
        {"error": "Required fields missing"},
        status=status.HTTP_400_BAD_REQUEST
    )
        
    if UserDetail.objects.filter(user_id=user_id).exists():
        return Response(
        {"error": "User ID already exists try different user id"},
        status=status.HTTP_400_BAD_REQUEST
    )   
        
    data = request.data.copy()
    data['password'] = hash_password(password)
 
        
    serializer = UserDetailModelSerializer(data=data)
    if serializer.is_valid():
       serializer.save()
       return Response(
                       {
                "message": "User Created successfully",
                "data": serializer.data
                       }
                       , status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

 

@api_view(['POST'])
def user_login(request):

    login_id = request.data.get("login_id")
    password = request.data.get("password")

    
    if not login_id:
        return Response(
            {"error": "Please enter email ID or User ID"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not password:
        return Response(
            {"error": "Please enter password"},
            status=status.HTTP_400_BAD_REQUEST
        )    

    try:
        user = UserDetail.objects.get(email=login_id)
    except UserDetail.DoesNotExist:
        
        try:
            user = UserDetail.objects.get(user_id=login_id)
        except UserDetail.DoesNotExist:   
            return Response(
            {"error": "Invalid User"},
            status=status.HTTP_400_BAD_REQUEST
             )

    if not verify_password(password, user.password):
        return Response(
            {"error": "Invalid Password"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = UserDetailModelSerializer(user)

    return Response(
        {
            "message": "Welcome",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )
        


