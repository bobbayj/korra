import re

from datetime import timedelta

from django import forms
from django.utils import timezone

from cersei.forms import BootstrappedForm

from .models import File, BadPasswordException, FileExpiredException


class UploadForm(BootstrappedForm):

    LIFETIME = (
        (1, "1 Hour"),
        (3, "3 Hours"),
        (5, "5 Hours"),
        (8, "8 Hours"),
        (12, "12 Hours"),
        (18, "18 Hours"),
        (24, "24 Hours"),
    )

    password = forms.CharField(
        widget=forms.widgets.PasswordInput, min_length=8)

    lifetime = forms.ChoiceField(
        required=False,
        choices=LIFETIME,
        help_text="The number of hours you want this file to remain on the "
                  "server"
    )

    delete_on_download = forms.BooleanField(
        required=False,
        initial=True,
        label="Delete the file after just one download"
    )

    file = forms.FileField()

    def store(self):

        lifetime = self.cleaned_data["lifetime"]

        f = File.objects.create(
            name=self.cleaned_data["file"].name,
            content_type=self.cleaned_data["file"].content_type,
            delete_on_download=bool(self.cleaned_data["delete_on_download"]),
            expires=(timezone.now() + timedelta(hours=int(lifetime)))
        )
        f.store(
            self.cleaned_data["file"],
            bytes(self.cleaned_data["password"], "utf-8")
        )

        return f.get_absolute_url()


class DownloadForm(BootstrappedForm):

    name = forms.CharField(widget=forms.widgets.HiddenInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    ACCEPTABLE_NAME_REGEX = re.compile(r"^[a-f0-9\-]{36}$")

    def __init__(self, *args, **kwargs):
        BootstrappedForm.__init__(self, *args, **kwargs)
        self.fields["password"].widget.attrs.update({"autocomplete": "off"})
        self.file = None
        self.file_data = None

    def clean(self):

        pk = self.cleaned_data.get("name")
        if not pk or not self.ACCEPTABLE_NAME_REGEX.match(pk):
            raise forms.ValidationError("Invalid name")

        try:
            self.file = File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise forms.ValidationError(
                "That file has been deleted or possibly never existed in the "
                "first place."
            )

        if not self.file:
            return self.cleaned_data

        try:
            self.file_data = self.file.fetch(
                bytes(self.cleaned_data.get("password"), "utf-8")
            )
        except (BadPasswordException, FileExpiredException) as e:
            raise forms.ValidationError(e)

        return self.cleaned_data
