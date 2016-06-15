from datetime import datetime, timedelta

from django import forms
from django.utils import timezone

from cersei.forms import BootstrappedForm
from .models import File


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
        label="Delete the file after just one download"
    )

    file = forms.FileField()

    def store(self):

        kwargs = {"delete_on_download": False}
        lifetime = self.cleaned_data["lifetime"]
        delete_on_download = self.cleaned_data["delete_on_download"]

        if lifetime:
            kwargs["expires"] = timezone.now() + timedelta(hours=int(lifetime))

        if delete_on_download:
            kwargs["delete_on_download"] = True

        f = File.objects.create(**kwargs)
        f.store(
            self.cleaned_data["file"],
            bytes(self.cleaned_data["password"], "utf-8")
        )

        return f.get_absolute_url()
