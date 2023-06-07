from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    # Post views
    path('', views.post_list, name='post list'),
    #path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_details,
         name='post_details'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('charts/', views.charts_view, name='charts'),
]
