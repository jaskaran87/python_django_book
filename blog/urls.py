from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$',views.post_list, name='post_list'),
    url(r'^abc$', views.PostListView.as_view(), name='post_list'),
    url(r'(?P<slug>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'(?P<post_id>\d+)/s$', views.post_share, name='post_share'),
]