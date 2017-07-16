# Korra

Transferring files securely is a pain in the ass, especially if you work in an
office environment where the technologies are heavily fragmented, and/or you're
working with users who are not particularly technically savvy.

The common denominator for many office environments consists of two tools:
websites and (unencrypted) email.  Slightly more advanced companies may make
use of IRC, Slack, and maybe some combination of Dropbox and Google Drive.
None of these tools make it easy to transfer files one-to-one safely &
securely, so I wrote this.  Do with it as you will.

![upload](https://raw.githubusercontent.com/danielquinn/korra/master/upload.png "Upload")
![success](https://raw.githubusercontent.com/danielquinn/korra/master/success.png "Success")
![download](https://raw.githubusercontent.com/danielquinn/korra/master/download.png "Download")


## The User Journey

1. Sender uploads file and gives it a password, and optionally provides
   a time limit value.
2. The server symmetrically encrypts the file and stores it locally.
3. The sender is redirected to a thank you page with a URL for the file.
4. The sender copy/pastes this URL into whatever channel they might have
   to communicate with their target user and passes on the password to
   them (hopefully) by some other means.
5. The recipient goes to the URL, types in the password, and gets the
   file.
6. Depending on the rules set by the sending user, the file is deleted
   once it's been downloaded, or is deleted after a fixed time.


## Installation

As Korra is effectively an anonymous file store, it isn't meant to be a public
web service, lest you run the risk of being an unwitting participant in
distribution of files you may not want to distribute.  Instead, this code is
meant to be plugged into a private server somewhere that's accessible within
your office and [secured with HTTPS](https://letsencrypt.org/).


### Setup


#### .env

Korra is configured by way of environment variables.  Handily, it populates its
environment by reading a file named `.env` out of the project root.  If you put
your values in there, Korra will use them at start-up.

* **SALT**: A long random string used to salt your file encryption.  Set this
  once and don't change it unless you're cool with any existing files being
  irretrievable.  The longer this string, the stronger the encryption, so about
  128 characters is a good place to start.
* **SECRET_KEY**: The Django secret key.  This should be a long random string.
  Don't change it once it's set.  A good length is about 64 characters.
* **MEDIA_ROOT**: Your Django media root.  See the [Django docs](https://docs.djangoproject.com/en/1.9/topics/files/)
  covering media files for more info here.
* **STATIC_ROOT**: Your Django static root.  Seed the [Django docs on staticfiles](https://docs.djangoproject.com/en/1.9/ref/contrib/staticfiles/#module-django.contrib.staticfiles)
  for more info.
* **DOMAIN**: The domain you're hosting this on.  If you're not using the
  sample gunicorn script though, you can skip this.
* **DATABASE_URL**: A standard database URL.  See below for details.

Here is an example `.env` file:

```
SALT="this is my salt value"
SECRET_KEY="this is my secret key"
MEDIA_ROOT="/app/media/"
STATIC_ROOT="/app/static/"
DOMAIN="korra.mydomain.tld"
```

Additionally, if you want to configure for a database other than sqlite, you
can specify the following along with the above:

```
DATABASE_URL="postgresql://my_user:my_password@my_db_host/my_db_name"
```

Lastly, you can also add to Django's internal `INSTALLED_APPS` value by setting
`INSTALLED_APPS` in your environment.  Separate each app with a `,`:

```
INSTALLED_APPS="my_app,my_other_app"
```


#### Docker

Assuming that you've got the code checked out at `/var/www/korra`, this is
what you need:

```
docker run \
  --name korra \
  -p 8000:8000 \
  -v /var/www/korra/:/app/ \
  -d danielquinn/korra
```


#### The Hard Way (not really)

For the most part, this is just a plain & simple Django project.  There's a
gunicorn sample file and a Systemd .service file to get you started.

But how exactly do you deploy this on say, your Ubuntu box at home running
Apache or Nginx?  For that, the only thing you really need to know is that this
is a standard Django project, so deploying this project should work just like
every other Django setup.  For details on how a typical Django project is
deployed, see [the Django documentation](https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/).


## Why Korra?

Given the nature of this project, I was looking for a name of a famous
medium between parties, someone who helped with communication, and I
settled on Nickelodeon's [Avatar](https://en.wikipedia.org/wiki/Avatar:_The_Last_Airbender).
However, given that that word can be ambiguous, I opted for [Korra](https://en.wikipedia.org/wiki/Korra),
in reference to the title character in the excellent sequel series
[The Legend of Korra](https://en.wikipedia.org/wiki/The_Legend_of_Korra).
