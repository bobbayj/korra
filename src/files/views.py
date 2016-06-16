from urllib.parse import quote

from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse

from .forms import UploadForm, DownloadForm


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


class DownloadView(FormView):

    form_class = DownloadForm
    template_name = "files/download.html"

    def get_initial(self):
        initial = FormView.get_initial(self)
        initial["name"] = self.kwargs["pk"]
        return initial

    def form_valid(self, form):

        r = HttpResponse(
            content=form.file_data,
            content_type=form.file.content_type
        )

        r["Content-Disposition"] = "attachment; filename={}".format(
            form.file.name
        )

        return r
