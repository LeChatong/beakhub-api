from django.shortcuts import render, get_list_or_404

# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status

from Apps.account.models import User
from Apps.account.serializers import UserSerializer
from Apps.core.models import UserAPIKey
from Apps.core.permissions import UserHasAPIKey


class UserListView(generics.ListCreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            get_list_or_404(
                self.get_queryset().all()
            ),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        try:
            user = User.objects.get(email=email)
            return Response({"Error": 'This mail address already used'}, status=status.HTTP_208_ALREADY_REPORTED)
        except User.DoesNotExist:
            pass
        try:
            user = User.objects.get(username=username)
            return Response({"Error": 'This username already used'}, status=status.HTTP_208_ALREADY_REPORTED)
        except User.DoesNotExist:
            pass
        try:
            user = User.objects.create_user(username, email, password)
        except User.DoesNotExist:
            return Response({"Error": 'Error Encoured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(
            user,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(
            get_object_or_404(
                self.get_queryset(),
                pk=pk
            ),
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None, *args, **kwargs):
        email = request.data.get('email', None)
        username = request.data.get('username', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        birth_date = request.data.get('birth_date', None)
        phone = request.data.get('phone', None)
        country = request.data.get('country', None)
        try:
            user = self.get_queryset().get(pk=pk)
        except User.DoesNotExist:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

        if email is not None:
            user.email = email
            user.save()
        if username is not None:
            user.username = username
            user.save()
        if first_name is not None:
            user.first_name = first_name
            user.save()
        if last_name is not None:
            user.last_name = last_name
            user.save()
        if birth_date is not None:
            user.birth_date = birth_date
            user.save()
        if phone is not None:
            user.phone = phone
            user.save()
        if country is not None:
            user.country = country
            user.save()
        serializer = self.get_serializer(
            user,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailsByUsernameView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, username):
        serializer = self.get_serializer(
            get_object_or_404(
                self.get_queryset(),
                username=username
            ),
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailsByEmailView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, email):
        serializer = self.get_serializer(
            get_object_or_404(
                self.get_queryset(),
                email=email
            ),
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
