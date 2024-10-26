from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import ToDo
from api.serializers import UserRegistrationSerializer, UserLoginSerializer, ListSerializer, ToDoListSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, NotFound
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
import jwt
from .utils import generate_access_token
from .authent import JWTAuthenticationFromCookie
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime


class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = (JWTAuthenticationFromCookie,)
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Register a new user",
        request_body=UserRegistrationSerializer,
        responses={201: openapi.Response('User registered successfully', UserRegistrationSerializer),
                   400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                access_token = generate_access_token(new_user)
                data = {'access_token': access_token}
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token, httponly=True)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = (JWTAuthenticationFromCookie,)
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Login a user",
        request_body=UserLoginSerializer,
        responses={200: openapi.Response('User logged in successfully', UserLoginSerializer),
                   401: 'Unauthorized'}
    )
    def post(self, request):
        email = request.data.get('email', None)
        user_password = request.data.get('password', None)

        if not user_password:
            raise AuthenticationFailed('A user password is needed.')

        if not email:
            raise AuthenticationFailed('A user email is needed.')

        user_instance = authenticate(username=email, password=user_password)

        if not user_instance:
            raise AuthenticationFailed('User not found.')

        if user_instance.is_active:
            user_access_token = generate_access_token(user_instance)
            response = Response()
            response.set_cookie(key='access_token', value=user_access_token, httponly=True)
            response.data = {
                'access_token': user_access_token
            }
            return response

        return Response({'message': 'Something went wrong.'})


class UserViewAPI(APIView):
    authentication_classes = (JWTAuthenticationFromCookie,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Retrieve user details",
        responses={200: openapi.Response('User details retrieved successfully', UserRegistrationSerializer),
                   401: 'Unauthorized'}
    )
    def get(self, request):
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(id=payload['user_id']).first()
        user_serializer = UserRegistrationSerializer(user)
        return Response(user_serializer.data)


class UserLogoutViewAPI(APIView):
    authentication_classes = (JWTAuthenticationFromCookie,)
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Logout user",
        responses={200: openapi.Response('User logged out successfully'),
                   204: 'No Content'}
    )
    def get(self, request):
        user_token = request.COOKIES.get('access_token', None)
        if user_token:
            response = Response()
            response.delete_cookie('access_token')
            response.data = {'message': 'Logged out successfully.'}
            return response
        response = Response()
        response.data = {'message': 'User is already logged out.'}
        return response


class UserToDoListView(generics.ListAPIView):
    serializer_class = ListSerializer
    authentication_classes = [JWTAuthenticationFromCookie]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'due_date']

    @swagger_auto_schema(
        operation_summary="List all ToDo items for authenticated user",
        responses={200: ListSerializer(many=True)}
    )
    def get_queryset(self):
        queryset = ToDo.objects.filter(user=self.request.user)

        due_date = self.request.query_params.get('due_date', None)
        if due_date:
            try:
                due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
                queryset = queryset.filter(due_date=due_date_obj)
            except ValueError:
                pass  # Handle invalid date format if needed

        return queryset


class CreateToDoView(generics.CreateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoListSerializer
    authentication_classes = [JWTAuthenticationFromCookie]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new ToDo item",
        request_body=ToDoListSerializer,
        responses={201: openapi.Response('ToDo item created successfully', ToDoListSerializer),
                   400: 'Bad Request'}
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailSerealizerView(generics.RetrieveAPIView):
    serializer_class = ToDoListSerializer
    authentication_classes = [JWTAuthenticationFromCookie]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a specific ToDo item",
        responses={200: ToDoListSerializer,
                   404: 'Task not found.'}
    )
    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    def get_object(self):
        try:
            return self.get_queryset().get(id=self.kwargs['pk'])
        except ToDo.DoesNotExist:
            raise NotFound('Task not found.')


class UpdateToDoView(generics.UpdateAPIView):
    serializer_class = ToDoListSerializer
    authentication_classes = [JWTAuthenticationFromCookie]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Update a specific ToDo item",
        request_body=ToDoListSerializer,
        responses={200: openapi.Response('ToDo item updated successfully', ToDoListSerializer),
                   404: 'Task not found.'}
    )
    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    def get_object(self):
        try:
            return self.get_queryset().get(id=self.kwargs['pk'])
        except ToDo:
            raise NotFound('Task not found.')

    def perform_update(self, serializer):
        serializer.save()


class DeleteToDoView(generics.DestroyAPIView):
    serializer_class = ToDoListSerializer
    authentication_classes = [JWTAuthenticationFromCookie]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Delete a specific ToDo item",
        responses={204: 'No Content',
                   404: 'Task not found.'}
    )
    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    def get_object(self):
        try:
            return self.get_queryset().get(id=self.kwargs['pk'])
        except ToDo.DoesNotExist:
            raise NotFound('Task not found.')
