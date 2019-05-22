"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin

from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from blog.apis import PostViewSet, CategoryViewSet
from blog.views import IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthorView
from config.views import LinkListView
from comment.views import CommentView

from blog.rss import LatestPostFeed
from blog.sitemap import PostSiteMap

from .custom_site import custom_site
from .autocomplete import CategoryAutocompleteView, TagAutocompleteView

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')

urlpatterns = [
                  path('super_admin/', admin.site.urls, name='super-admin'),
                  path('admin/', custom_site.urls, name='admin'),
                  path('xadmin/', xadmin.site.urls, name='xadmin'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('api/', include(router.urls)),
                  path('api/docs/', include_docs_urls(title='typeidea apis')),

                  re_path(r'^$', cache_page(60 * 20, key_prefix='sitemap_cache_')(IndexView.as_view()), name='index'),
                  re_path(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
                  re_path(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
                  re_path(r'^post/(?P<post_id>\d+)/$', PostDetailView.as_view(), name='post-detail'),
                  re_path(r'^links/$', LinkListView.as_view(), name='links'),
                  re_path(r'^comment/$', CommentView.as_view(), name='comment'),
                  re_path(r'^search/$', SearchView.as_view(), name='search'),
                  re_path(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
                  re_path(r'^rss|feed$', LatestPostFeed(), name='rss'),
                  re_path(r'^sitemap\.xml$', cache_page(60 * 20, key_prefix='sitemap_cache_')(sitemap_views.sitemap),
                          {'sitemaps': {'posts': PostSiteMap}}),
                  re_path(r'^category-autocomplete/$', CategoryAutocompleteView.as_view(),
                          name='category-autocomplete'),
                  re_path(r'^tag-autocomplete/$', TagAutocompleteView.as_view(), name='tag-autocomplete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path(r'__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk'))
    ]
