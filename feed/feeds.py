from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.urls import reverse

class LatestPostsFeed(Feed):
    title = "Feed"
    link = ""
    description = "Curious sharing"

    def items(self):
        return Post.objects.filter(status=1)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)

    def item_link(self, item):
         return reverse("post_detail", args=[item.slug])
