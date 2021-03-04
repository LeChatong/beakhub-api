from django.shortcuts import render, get_list_or_404

# Create your views here.
from requests import Response
from rest_framework import generics, status

from Apps.account.models import User
from Apps.account.serializers import UserSerializer
from Apps.core.models import UserAPIKey
from Apps.core.permissions import UserHasAPIKey


class UserCreateView(generics.CreateAPIView):
    permission_classes = [UserHasAPIKey]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        try:
            user = User.objects.get(email=email)
            return Response({"Error": _('This mail address already used')}, status=status.HTTP_208_ALREADY_REPORTED)
        except user.DoesNotExist:
            pass
        try:
            user = User.objects.get(username=username)
            return Response({"Error": _('This username already used')}, status=status.HTTP_208_ALREADY_REPORTED)
        except user.DoesNotExist:
            pass
        try:
            user = User.objects.create_user(username, email, password)
        except user.DoesNotExist:
            return Response({"Error": _('Error Encoured')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(
            user,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        serializer = self.get_serializer(
            get_list_or_404(
                self.get_queryset().all()
            ),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
