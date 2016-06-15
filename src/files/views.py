from urllib.parse import quote

from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse

from .forms import UploadForm


class UploadView(FormView):

    form_class = UploadForm
    template_name = "files/upload.html"

    def form_valid(self, form):
        return HttpResponseRedirect("{}?url={}".format(
            self.get_success_url(),
            quote(form.store())
        ))

    def get_success_url(self):
        return reverse("uploaded")


class UploadedView(TemplateView):

    template_name = "files/uploaded.html"

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context["url"] = self.request.build_absolute_uri(
            self.request.GET.get("url")
        )
        return context
