from .views import CreateView, LoginAPIView, ChangeAPIView
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = {
    url(r'user/$', CreateView.as_view(), name="create"),
    url(r'login/$', LoginAPIView.as_view(), name='login'),
    url(r'changeimage/$', ChangeAPIView.as_view(), name='change'),
}

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)