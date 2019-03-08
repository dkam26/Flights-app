from rest_framework import generics
from rest_framework.views import APIView
from user.models import User
from rest_framework.authtoken.models import Token
from user.serializers import UserSerializer, UserLoginSerializer, ChangeSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from user.backends import MyAuthBackend
from rest_framework import permissions
from rest_framework.response import Response
from user.serializers import UserSerializer, ChangeSerializer
from rest_framework import mixins, generics
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import status
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Create your views here.


class CreateView(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = (UserSerializer, ChangeSerializer)
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        passport_photograh_url = cloudinary.uploader.upload(request.FILES['passport_photograh'])
        request.data['passport_photograh'] = passport_photograh_url['secure_url']
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response('Wrong format/Email already exists')
    def put(self, request, *args, **kwargs):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            passport_photograh = request.FILES['passport_photograh']
            passport_photograh_url = cloudinary.uploader.upload(passport_photograh)
            if passport_photograh:
                user = User.objects.get(id=user_id)
                user.passport_photograh = passport_photograh_url['secure_url']
                user.save()
                Response(user)
            else:
                Response('Provide valid image')
        return Response('No token provided')
    def delete(self, request, *args, **kwargs):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            user = User.objects.get(id=user_id)
            user.passport_photograh = ''
            user.save()
            Response(user)
        return Response('No token provided')

class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self, request, format=None):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        AuthBack = MyAuthBackend()
        user = AuthBack.authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                token,_ = Token.objects.get_or_create(user=user)
                return Response({'token':token.key}, status=HTTP_200_OK)
            else:
                return Response({'Message':'Invalid credientals'},status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'Message':'Invalid credientals'},status=HTTP_400_BAD_REQUEST)

class ChangeAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser,FormParser)
    def put(self, request, format=None):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            serializer = ChangeSerializer(data=request.data['passport_photograh'])
            passport_photograh = request.FILES['passport_photograh']
            user = User.objects.get(id=user_id)
            # user.passport_photograh = passport_photograh
            # user.save()
            return Response(passport_photograh )
        return Response('No token provided')
