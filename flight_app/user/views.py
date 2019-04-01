from rest_framework import generics
from rest_framework.views import APIView
from flight_app.user.models import User
from rest_framework.authtoken.models import Token
from flight_app.user.serializers import UserSerializer, UserLoginSerializer, ChangeSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from flight_app.user.backends import MyAuthBackend
from rest_framework import permissions
from rest_framework.response import Response
from flight_app.user.serializers import UserSerializer, ChangeSerializer
from rest_framework import mixins, generics
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import status
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flight_app.tasks import send_notification_email_task
from datetime import datetime, timedelta
from django.utils.timezone import now
# Create your views here.


class CreateView(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = (UserSerializer, ChangeSerializer)
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        image_url = request.FILES['passport_photograh']
        if image_url.name.endswith('.jpg') or image_url.name.endswith('.png'):
            passport_photograh_url = cloudinary.uploader.upload(request.FILES['passport_photograh'])
            request.data['passport_photograh'] = passport_photograh_url['secure_url']
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                tomorrow = datetime.utcnow() + timedelta(days=1)
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'Message':'Wrong format/Email already exists'})
        return Response({'Message':'Invalid image type.Only .jpg and .png images allowed!'})
    def put(self, request, *args, **kwargs):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            if user_id:
                passport_photograh = request.FILES['passport_photograh']
                if passport_photograh.name.endswith('.jpg') or passport_photograh.name.endswith('.png'):
                    passport_photograh_url = cloudinary.uploader.upload(passport_photograh)
                    user = User.objects.get(id=user_id)
                    user.passport_photograh = passport_photograh_url['secure_url']
                    user.save()
                    return Response({'Message':'Image successfully changed'})
                else:
                    return Response({'Message':'Invalid image type.Only .jpg and .png images allowed!'})
            else:
                return Response({'Message':'Invalid Token'})
        return Response({'Message':'No token provided'})
    def delete(self, request, *args, **kwargs):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            if user_id:
                user = User.objects.get(id=user_id)
                user.passport_photograh = ''
                user.save()
                return Response({'Message':'Image successfully removed'})
            else:
                return Response({'Message':'Invalid token'})

        return Response({'Message':'No token provided'})

class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self, request, format=None):
        if list(request.data.keys()) == ['email', 'password']:
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
        return Response({'Message':'Invalid json keys'},status=HTTP_400_BAD_REQUEST)

