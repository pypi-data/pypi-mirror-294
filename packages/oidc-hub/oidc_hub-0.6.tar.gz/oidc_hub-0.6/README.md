# OpenID Connect Hub

The `oidc_hub` package acts as an identity provider, integrating OpenID Connect to streamline Identity and Access Management (IAM). 

This package provides user authentication, password resets, and invitations while providing secure identity verification and profile management. 

Using OpenID Connect’s standardized protocols, `oidc_hub` manages user identities and access, enhancing both security and operational efficiency for Djangonauts.

## Installation

```shell
pip install oidc-hub
```

### Configuration

#### Required

Add `oidc_hub` and `oidc_provider` to your `INSTALLED_APPS` in the Django project's settings:

```python
INSTALLED_APPS = [
  "oidc_hub.accounts",
  "oidc_hub.admin",
  "django.contrib.admin",
  # ...
  "django.contrib.staticfiles",
  "oidc_provider",
]
```

Then, we can use the package root urlconf:

```python
ROOT_URLCONF = "oidc_hub.urls"
```

#### Optional

To support multiple languages in our application, we should configure internationalization (i18n) settings:

```python
LANGUAGE_CODE = "fr"
LANGUAGES = (
  ('fr', _('French')),
  ('en', _('English'))
)
TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True
```

### Migrations

Run migrations to create the required database tables:

```shell
./manage.py migrate
```

The first time you migrate, an administrator account will be created according to the settings you have specified in a settings module.

The initial migration will use `ADMIN_USERNAME`, `ADMIN_EMAIL` and `ADMIN_PASSWORD` settings or their default values if these settings are not specified.

## Webserver

#### Development

Start the Django development server.

```shell
./manage.py runserver
```

## License

This project is licensed under the AGPLv3 License - see the [LICENSE.md](LICENSE.md) file for details.
