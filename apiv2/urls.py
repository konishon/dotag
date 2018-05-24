from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, ReportRatingCreateView, register_by_access_token
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = {
    url(r'^apiv2/bucketlists/$', CreateView.as_view(),name="create"),
    url(r'^apiv2/reportrating/$', ReportRatingCreateView.as_view(),name="create_report"),
    url(r'^apiv2/get-token/', obtain_auth_token),
    url(r'^api/fbtest/(?P<backend>[^/]+)/', register_by_access_token),
    url('', include('social_django.urls', namespace='social'))
}

urlpatterns = format_suffix_patterns(urlpatterns)