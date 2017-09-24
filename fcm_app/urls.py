from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'fcm_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^import_map$', views.import_fcm, name='import_map'),
    url(r'^browse$', views.browse, name='browse'),
    url(r'^view-fcm/(?P<fcm_id>[\d-]+)/$', views.view_fcm, name='view_fcm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
