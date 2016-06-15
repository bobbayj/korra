import base64
import uuid

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from django.conf import settings
from django.db import models


class File(models.Model):

    id = models.UUIDField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(blank=True, null=True)
    delete_on_download = models.BooleanField(default=True)

    @staticmethod
    def store(file_handle, password):
        salt = settings.CERSEI_SALT
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        token = f.encrypt(file_handle.read())
        print(token)
        # with open("/tmp/{}", "wb") as f:
        #     f.write(token)
        f.decrypt(token)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        models.Model.save(self, *args, **kwargs)

    def get_absolute_url(self):
        return "/download/{}".format(self.pk)
