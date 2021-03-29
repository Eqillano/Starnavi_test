from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Profile
from .serializers import RegistrationSerializer
import jwt
import datetime

# Create your views here.


class TokenAuthenticationView(ObtainAuthToken):

    def post(self, request):
        result = super(TokenAuthenticationView, self).post(request)
        currentUserModel = Profile
        user = currentUserModel.objects.get(
            email=request.data['email'])
        update_last_login(None, user)
        return result


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        username = request.data['username']
        profile = Profile.objects.filter(email=email).first()
        if profile is None:
            raise AuthenticationFailed('User not found')

        if not profile.check_password(password):
            raise AuthenticationFailed('Incorrent password')

        payload = {
            'id': profile.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class ProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unathenticated')

        profile = Profile.objects.filter(id=payload['id']).first()
        serializer = RegistrationSerializer(profile)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
