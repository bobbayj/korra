import base64
import os
import uuid

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class BadPasswordException(Exception):
    pass


class FileExpiredException(Exception):
    pass


class File(models.Model):

    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=128)
    content_type = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(blank=True, null=True)
    delete_on_download = models.BooleanField(default=True)

    def store(self, file_handle, password):
        with open(self.get_path(), "wb") as f:
            f.write(self._get_fernet(password).encrypt(file_handle.read()))

    def get_path(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.pk))

    def fetch(self, password):

        if self.expires and timezone.now() > self.expires:
            self.delete()
            raise FileExpiredException("This file is no longer available")

        try:
            with open(self.get_path(), "rb") as f:
                return self._get_fernet(password).decrypt(f.read())
        except InvalidToken:
            raise BadPasswordException("Invalid password")

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        models.Model.save(self, *args, **kwargs)

    def get_absolute_url(self):
        return reverse("download", kwargs={"pk": self.pk})

    def delete(self, *args, **kwargs):

        try:
            os.unlink(self.get_path())
        except FileNotFoundError:
            pass

        models.Model.delete(self, *args, **kwargs)

    def _get_fernet(self, password):
        return Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=settings.CERSEI_SALT,
            iterations=100000,
            backend=default_backend()
        ).derive(password)))
