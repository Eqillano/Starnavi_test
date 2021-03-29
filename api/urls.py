from django.urls import path, include
from .views import post_action_view, PostCreateView, PostListView, PostUpdateView, PostAnalyticsLikesView, PostDeleteView


urlpatterns = [
    path('post_action/', post_action_view, name='post-action'),
    path('post-create/', PostCreateView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post_analytics/date_from=<date_from>&date_to=<date_to>/',
         PostAnalyticsLikesView.as_view(), name='likes'),

]
