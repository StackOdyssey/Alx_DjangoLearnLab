from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    tags = TaggableManager()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        # Redirect to the detail page of this post
        return reverse('post-detail', kwargs={'pk': self.pk})


def user_profile_upload_path(instance, filename):
    return f'profiles/user_{instance.user_id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_upload_path, blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Many-to-many on Post (in a migration-safe way, add after Tag exists)
Post.add_to_class('tags', models.ManyToManyField(Tag, related_name='posts', blank=True))

