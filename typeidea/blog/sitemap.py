from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .models import Post


class PostSiteMap(Sitemap):
    changefreq = "always"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('post-detail', args=[obj.pk])
