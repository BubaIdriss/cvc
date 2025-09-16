from django.db import models
from django.contrib.auth import get_user_model
import uuid
from cloudinary.models import CloudinaryField

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    cover_img = CloudinaryField("Profile-img/cover_images", blank=True)
    profile_img = CloudinaryField("Profile-img/profie_images", blank=True)

    def __str__(self):
        return f"{self.user.username} | Profile"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    post_caption = models.TextField(blank=True)
    post_image = CloudinaryField("Posts-img/post_images", blank=True)
    url1 = models.URLField(blank=True)
    url2 = models.URLField(blank=True)
    url3 = models.URLField(blank=True)
    user_ip = models.CharField(max_length=15, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | Post"
    
class Comment(models.Model):
    users = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment_id = models.AutoField(primary_key=True)
    comment_caption = models.TextField()
    comment_url = models.URLField(blank=True)
    comment_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.users} on {self.comment_post.post_id} | {self.comment_caption[:20]}"