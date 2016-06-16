from django.conf.urls import url
from django.contrib import admin

from files.views import UploadView, UploadedView, DownloadView

urlpatterns = [
    url(r"^upload$", UploadView.as_view(), name="upload"),
    url(r"^upload/success$", UploadedView.as_view(), name="uploaded"),
    url(r"^download/(?P<pk>.*)", DownloadView.as_view(), name="download"),
    url(r'^admin/', admin.site.urls),
]
