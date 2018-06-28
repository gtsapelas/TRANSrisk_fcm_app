from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'fcm_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^import_map$', views.import_fcm, name='import_map'),
    url(r'^create_map$', views.create_fcm, name='create_map'),
    url(r'^browse$', views.browse, name='browse'),
    url(r'^view-fcm/(?P<fcm_id>[\d-]+)/$', views.view_fcm, name='view_fcm'),
    url(r'^view-fcm-concept/(?P<fcm_id>[\d-]+)/$', views.view_fcm_concept, name='view_fcm_concept'),
    url(r'^view-fcm-concept-info/(?P<fcm_id>[\d-]+)/(?P<concept_id>[\d-]+)/$', views.view_fcm_concept_info, name='view_fcm_concept_info'),
    url(r'^my-fcms/$', views.my_fcms, name='my_fcms'),
    url(r'^edit-fcm/(?P<fcm_id>[\d-]+)/$', views.edit_fcm, name='edit_fcm'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
