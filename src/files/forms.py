import re

from datetime import timedelta

from django import forms
from django.utils import timezone

from korra.forms import BootstrappedForm

from .models import File, BadPasswordException, FileExpiredException


class UploadForm(BootstrappedForm):

    LIFETIME = (
        (None, ""),
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
    password_confirmation = forms.CharField(
        widget=forms.widgets.PasswordInput,
        min_length=8,
        label="Confirm Password"
    )

    lifetime = forms.ChoiceField(
        required=False,
        choices=LIFETIME,
        help_text="The number of hours you want this file to remain on the "
                  "server before it's automatically deleted."
    )

    delete_on_download = forms.BooleanField(
        required=False,
        initial=True,
        label="Delete this file immediately after it's downloaded."
    )

    file = forms.FileField()

    def clean(self):
        r = self.cleaned_data
        password1 = r.get("password")
        password2 = r.get("password_confirmation")

        if not password1 == password2:
            raise forms.ValidationError("The passwords do not match")

    def store(self):

        lifetime = self.cleaned_data["lifetime"]
        delete_on_download = bool(self.cleaned_data["delete_on_download"])

        kwargs = {
            "name": self.cleaned_data["file"].name,
            "content_type": self.cleaned_data["file"].content_type,
            "delete_on_download": delete_on_download,
        }

        if lifetime:
            kwargs["expires"] = timezone.now() + timedelta(hours=int(lifetime))

        f = File.objects.create(**kwargs)
        f.store(
            self.cleaned_data["file"],
            bytes(self.cleaned_data["password"], "utf-8")
        )

        return f.get_absolute_url()


class DownloadForm(BootstrappedForm):

    name = forms.CharField(widget=forms.widgets.HiddenInput)
    password = forms.CharField(
        widget=forms.widgets.PasswordInput,
        help_text="The password for the encrypted file."
    )

    ACCEPTABLE_NAME_REGEX = re.compile(r"^[a-f0-9\-]{36}$")

    def __init__(self, *args, **kwargs):
        BootstrappedForm.__init__(self, *args, **kwargs)
        self.fields["password"].widget.attrs.update({
            "autocomplete": "off",
            "placeholder": "Password"
        })
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
                "That file has been deleted or may never existed in the first "
                "place."
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
