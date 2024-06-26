"""All models."""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Model Group."""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        """Visualisate Group."""
        return self.title


class Post(models.Model):
    """Model Post."""

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='group_posts',
        verbose_name='Сообщество',
        help_text='Выберите сообщество')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    def __str__(self):
        """Visualisate Post."""
        return self.text


class Comment(models.Model):
    """Model Comment."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        """Meta Comment."""

        ordering = ['created']


class Follow(models.Model):
    """Model Follow."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        null=False
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        null=False,
    )

    class Meta:
        """Meta Follow."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name="unique_followers")
        ]
