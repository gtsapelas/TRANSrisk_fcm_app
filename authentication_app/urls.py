from django.conf.urls import url
from . import views

app_name = 'authentication_app'
urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
