from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, ReportRatingCreateView, register_by_access_token, ReportView, HomeView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = {
    url(r'^$', HomeView.as_view()),  
    url(r'^api/bucketlists/$', CreateView.as_view(),name="create"),
    url(r'^api/rating/$', ReportRatingCreateView.as_view(),name="rating-upload"),
    url(r'^api/get-token/', obtain_auth_token),
    url(r'^api/fbtest/(?P<backend>[^/]+)/', register_by_access_token),
    url(r'^report/$', ReportView.as_view(), name='report-upload'),
    url('', include('social_django.urls', namespace='social'))
}

urlpatterns = format_suffix_patterns(urlpatterns)