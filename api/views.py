from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from .models import Post, PostLike
from .serializers import PostCreateSerializer, PostActionSerializer, PostListSerializer, PostLikeSerializer
from rest_framework import filters

# Create your views here.


class PostCreateView(generics.CreateAPIView):
    model = Post
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostCreateSerializer


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    """ def get_queryset(self):
        profile = self.request.profile
        print(profile)
        return Post.objects.filter(profile=profile) """


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_action_view(request, *args, **kwargs):
    print(request.POST)
    serializer = PostActionSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get('id')
        action = data.get('action')
        print(data)

        qs = Post.objects.filter(id=post_id)

        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == 'like':
            if request.user not in obj.likes.all():
                obj.likes.add(request.user)
                obj.save()
            else:
                return Response({"You have already liked this post"})

        elif action == 'unlike':
            if request.user not in obj.likes.all():
                return Response({"You havent liked this post yet"})
            else:
                obj.likes.remove(request.user)
                obj.save()

    return Response({'Successfully ' + action + 'd'})


class PostAnalyticsLikesView(generics.ListAPIView):
    serializer_class = PostLikeSerializer

    def get(self, request, *args, **kwargs):
        likes = PostLike.objects.filter(
            pub_date__range=[kwargs['date_from'], kwargs['date_to']])
        return Response('There have been ' + str(len(likes)) + " likes in the the selected period")
