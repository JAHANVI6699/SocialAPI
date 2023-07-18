from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
# Create your views here.
from rest_framework import filters, generics, mixins, permissions,viewsets
from rest_framework.response import Response

from .models import FriendRequest, User
from .serializers import FriendRequestSerializer, UserSerializer


class UserCreateAPIView(viewsets.ModelViewSet):
   
   def get_permissions(self):
      permission_classes = [permissions.IsAuthenticated]
      if self.action == 'create':
         permission_classes = [permissions.AllowAny]
      return super().get_permissions()

   queryset = User.objects.all()
   serializer_class = UserSerializer
   filter_backends = [filters.SearchFilter]
   search_fields = ['email','first_name']


class UserLoginAPIView(generics.GenericAPIView):

   permission_classes = [permissions.AllowAny]
   serializer_class = UserSerializer
   queryset = User.objects.all()

   def post(self, request):
      serializer = UserSerializer
      user = authenticate(email=request.POST['email'], password=request.POST['password'])
      if user:
         serializer = self.get_serializer(user)
         return Response(serializer.data)

      return Response({'detail': 'User not found'}, status=400)

class FriendRequestAPIView(generics.GenericAPIView):
   serializer_class = FriendRequestSerializer
   permission_classes = [permissions.IsAuthenticated]
   queryset = FriendRequest.objects.all()
   def post(self, request):
      to_user_id = request.data.get('to_user_id')

      if not to_user_id:
         return Response({'detail': 'Missing to_user_id'}, status=400)

      to_user = User.objects.filter(id=to_user_id).first()

      if not to_user:
         return Response({'detail': 'User not found'}, status=404)

      from_user = request.user

      if from_user == to_user:
         return Response({'detail': 'You cannot send a friend request to yourself'}, status=400)

      friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)

      if not created:
         return Response({'detail': 'Friend request already sent'}, status=400)

      serializer = self.get_serializer(friend_request)
      return Response(serializer.data)

   def patch(self, request, pk):
      friend_request = FriendRequest.objects.filter(to_user=pk).first()

      if not friend_request:
         return Response({'detail': 'Friend request not found'}, status=404)

      if friend_request.to_user != request.user:
         return Response({'detail': 'You do not have permission to perform this action'}, status=403)

      action = request.data.get('action')

      if action == 'accept':
         friend_request.is_accepted = True
         friend_request.save()

         return Response({'detail': 'Friend request accepted'})

      elif action == 'reject':
         friend_request.delete()
         return Response({'detail': 'Friend request rejected'})

      return Response({'detail': 'Invalid action'}, status=400)
