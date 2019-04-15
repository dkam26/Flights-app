from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from flight_app.flights.views import ListFlightView, CreateView, DetailsView, WelcomeView


urlpatterns = {
    url(r'welcome/$',WelcomeView.as_view(), name='Welcome'),
    url(r'flights/$',ListFlightView.as_view(), name='flights'),
    url(r'book/flight/$',CreateView.as_view(), name='book flight'),
    url(r'user/flights/$',DetailsView.as_view(), name= 'user flights')
}

urlpatterns = format_suffix_patterns(urlpatterns)