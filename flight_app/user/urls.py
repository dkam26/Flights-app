from .views import CreateView
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = {
    url(r'user/$', CreateView.as_view(), name="create"),

}

urlpatterns = format_suffix_patterns(urlpatterns)