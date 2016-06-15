from django.conf.urls import url
from django.contrib import admin

from files.views import UploadView, UploadedView

urlpatterns = [
    url(r"^upload$", UploadView.as_view(), name="upload"),
    url(r"^upload/success$", UploadedView.as_view(), name="uploaded"),
    url(r'^admin/', admin.site.urls),
]
