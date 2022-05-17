from rest_framework.views import APIView 
from rest_framework.views import Response
from rest_framework import status, filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles_api import serializers, models, permissions

class HelloApiView(APIView):
    # API VIEW TEST 
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        # get list , features of API VIEW
        
        an_apiview = [
            'We Use HTTp like function (get , post , put , delete)',
            'its likea view in django',
            'give us more control about the logic in the app',
            'its mapped manually'
        ]
        return Response({'message': 'Hello', 'an_apiview': an_apiview})
    
    def post(self, request):
        # create was god message with our song
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            song = serializer.validated_data.get('song')
            message = f' The Song {song} Was Really God '
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
    def put(self, request, pk=None):
        # when we update an object with put
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        # handle partial update of an object
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        # delete an object
        return Response({'method': 'DELETE'})
    
class HelloViewSet(viewsets.ViewSet):
    #Test Api View Set
    serializer_class = serializers.HelloSerializer
    
    def list(self, request):
        #return a hello message
        a_viewset = [
            'uses actions (list , create , retrieve , update , partial_update)',
            'automatically maps to URLs using Routers',
            'provides more functionality with less code'
        ]
        return Response({'message': 'Hi you stupid bastard ', 'a_viewset': a_viewset})
    
    def create(self, request):
        #create a new hello message
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            song = serializer.validated_data.get('song')
            message = f'Hello {song}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self, request, pk=None):
        #handle getting an object by its ID
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        #handle updating an object
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        #handle updating part of an object
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        #handle removing an object
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    #Handle creating and updating profiles
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permissions_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    #Handle creating user authentication tokens
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    #Handles creating, reading and updating profile feed items
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticatedOrReadOnly)
    
    def perform_create(self, serializer):
        #sets the user profile to the logged in user
        serializer.save(user_profile=self.request.user)