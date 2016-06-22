from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from files.views import UploadView, UploadedView, DownloadView

urlpatterns = [
    url(r"^$", UploadView.as_view(), name="upload"),
    url(r"^success$", UploadedView.as_view(), name="uploaded"),
    url(r"^download/(?P<pk>.*)", DownloadView.as_view(), name="download"),
    url(r"^about", TemplateView.as_view(template_name="korra/about.html"), name="about"),
    url(r'^admin/', admin.site.urls),
]
