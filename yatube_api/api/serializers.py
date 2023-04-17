"""Serializers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer."""

    class Meta:
        """Meta group serializer."""

        model = Group
        fields = ('__all__')


class PostSerializer(serializers.ModelSerializer):
    """Post serializer."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        """Meta post serializer."""

        model = Post
        fields = ('__all__')
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        """Meta comment serializer."""

        model = Comment
        fields = ('__all__')
        read_only_fields = (
            'post',
            'created',
        )


class FollowSerializer(serializers.ModelSerializer):
    """Follow serializer."""

    user = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        """Meta follow serializer."""

        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate(self, data):
        """Only one time follow check."""
        user = self.context['request'].user
        follow_obj = data['following']
        if user == follow_obj:
            raise serializers.ValidationError(
                'Подписываться на себя нельзя!'
            )
        if Follow.objects.filter(
            user=User.objects.get(username=user),
            following=User.objects.get(username=follow_obj)
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписались'
            )
        return data
