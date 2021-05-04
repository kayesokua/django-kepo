from django.db import models
from django.contrib.auth.models import User
import readtime

STATUS = ((0, "Draft"), (1, "Publish"))

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    img = models.ImageField(upload_to="media/myfeed")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts", default=1
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", kwargs={"author": str(self.author.username), "slug": str(self.slug)})
    
    def get_read_time(self):
       result = readtime.of_text(self.content)
       return result.text

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_comments", default=1
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.commenter)