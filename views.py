
from typing import Any
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets, mixins
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed

# Local modules imports
from sts import serializers as userserializer, emails, models

# Django imports
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import datetime


class Signup(APIView):
    """
    This API is used to signup (register a new user)
    Provide email, password and confirm password and then verify your account via the code sent to the email 
    Permissions: Allowed for all
    """

    permission_classes = (permissions.AllowAny, )
    serializer_classes = userserializer.SignupSerializer

    def post(self, request):

        try:
            data = request.data
            serializer = self.serializer_classes(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
        
            emails.send_otp_via_email(serializer.data['email'])
        
        except serializers.ValidationError as e:
            return Response(e.detail, status = status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message":"Successfully done, please check your email to verify your account"
            }, status = status.HTTP_200_OK)


class VerifyAccount(APIView):
    """
    This API is used to verify user's account 
    Provide email and OTPCode to verify the account and then login using the account
    Permissions: Allowed for all
    """
    serializer_classes = userserializer.VerifyAccountSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_classes(data = data)
            
            if serializer.is_valid(raise_exception=True):
                #? Get the entered email and OTP code to verify validation
                email = serializer.data['email']
                otp = serializer.data['otp']
    
                user = models.User.objects.filter(email = email)
                
                #? Check if the entered email is valid 
                if not user.exists():
                    return Response({
                        "error":"Invalid email"
                        }, status = status.HTTP_400_BAD_REQUEST)
              
                user = user.first()

                #? Check if the entered OTP code matches the sent code 
                if user.otp != otp:
                   
                    return Response({
                        "error":"Wrong verification code"
                        }, status = status.HTTP_400_BAD_REQUEST) 
                
                user.is_verified = True #? Update user's account status and save it
                user.otp = None #? Delete the otp after verification
                user.save()

        #? Check for validation errors (otp length > 6, otp is not digit)
        except serializers.ValidationError as validation_error: 
            return Response(validation_error.detail
                            , status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            
            return Response({
                "error": "Internal server error"
                }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        return Response({
                "message":"Account verified, you can login now"
                }, status = status.HTTP_200_OK)


class LogInAPI(TokenObtainPairView):
    """
    This API is used to Login in the website
    Provide email, password and you'll get the refresh token and access token
    Permissions: Allowed for all users
    """
    serializer_class = userserializer.LogInSerializer
    permission_classes = ( )
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        
        #? If either email or password is wrong raise a message error 
        except AuthenticationFailed as e:
            return Response({
                'message': e.detail
                }, status = status.HTTP_401_UNAUTHORIZED)


class UserData(generics.ListAPIView):
    serializer_class = userserializer.UserDataSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = models.User.objects
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK) 
    

class CreateOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request):
        serializer = userserializer.TripSerializer(data=request.data)
        if serializer.is_valid():

            available_captains = models.Captain.objects.filter(is_available=True)
            captain = available_captains.first()  
            client = request.user
            start = client.location

            trip = serializer.save(client_ID=request.user, captain_ID=captain)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListOrders(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
    serializer_class = userserializer.TripSerializer
    queryset = models.Trip.objects
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK) 


class AddCaptainView(APIView):
    permission_classes = (permissions. IsAdminUser, )  # Ensure only admin users can access

    def post(self, request):
        serializer = userserializer.CaptainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveCaptainView(generics.DestroyAPIView):
    permission_classes = (permissions. IsAdminUser, ) # Ensure only admin users can access

    def delete(self,request, captain_id):
        queryset = models.Captain.objects.get(pk=captain_id)
        queryset.delete()
        return Response({"done":"Deleted successfuly"},status = status.HTTP_204_NO_CONTENT)
        

class UserTripDataView(APIView):
    permission_classes = (permissions.AllowAny, )  # Ensure only admins can access

    def get(self, request, trip_id):
        try:
            trip = models.Trip.objects.get(pk=trip_id)
            user = trip.client_ID  # Assuming User is linked to Trip through client_ID field
            serializer = userserializer.UserOrderSerializer(user)
            return Response(serializer.data)
        except models.Trip.DoesNotExist:
            return Response({'error': 'Trip not found.'}, status=status.HTTP_404_NOT_FOUND)
        except models.User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        

class TripStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def patch(self, request, trip_id, action):
        if action not in ('accept', 'reject'):
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trip = models.Trip.objects.get(pk=trip_id)

            if action == 'accept':
                trip.status = 'ACCEPTED'  # Update status (optional)
            else:
                trip.status = 'REJECTED'  # Update status (optional)
            trip.save()

            serializer = userserializer.TripSerializer(trip)
            return Response({'done':'your order is accepted'},status=status.HTTP_200_OK)
        except models.Trip.DoesNotExist:
            return Response({'error': 'Trip not found.'}, status=status.HTTP_404_NOT_FOUND)