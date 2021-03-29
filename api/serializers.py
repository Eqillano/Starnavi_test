from .models import Post, Profile, PostLike
from rest_framework import serializers
from profiles.models import Profile
from rest_framework.fields import CurrentUserDefault

POST_ACTION_OPTIONS = ['like', 'unlike']


class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in POST_ACTION_OPTIONS:
            raise serializers.ValidationError('This is not a valid action')
        return value


class PostCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = [
            'id', 'text', 'profile'
        ]

    """   def save(self):
        access_token = self.request.META.get('TOKEN')
        profile = Token.objects.filter(token=access_token)
        text = self.validated_data['text']
        return self.validated_data """


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = (
            'user', 'post', 'timestamp',
        )
