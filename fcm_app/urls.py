from django.conf.urls import url
from . import views

app_name = 'fcm_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    #url(r'^(?P<var_name>[0-9]+)/$', views.detail, name='detail'), 
    #(r'^(?P<var_name>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]