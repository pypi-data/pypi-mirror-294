![Community-Project](https://gitlab.com/softbutterfly/open-source/open-source-office/-/raw/master/assets/dynova/dynova-open-source--banner--community-project.png)

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)

![PyPI - Supported versions](https://img.shields.io/pypi/pyversions/django-sb-codefield)
![PyPI - Package version](https://img.shields.io/pypi/v/django-sb-codefield)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-sb-codefield)
![PyPI - MIT License](https://img.shields.io/pypi/l/django-sb-codefield)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fe5644bd3a114473879a304321a68f3e)](https://app.codacy.com/gl/softbutterfly/django-sb-codefield/dashboard?utm_source=gl&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

# Django CodeField

Use codemirror2 widget directly in Django models, forms and admin.

## Requirements

- Python 3.10 or higher but lower than 4.0.0
- Django lower than 6.0.0
- django-codemirror2 lower than 1.0.0

## Install

```bash
pip install django-sb-codefield
```

## Usage

Add `codemirror2` and `django_sb_codefield` to your `INSTALLED_APPS` settings

```
INSTALLED_APPS = [
  # ...
  "codemirror2",
  "django_sb_codefield",
]
```

## Docs

- [Ejemplos](https://gitlab.com/softbutterfly/open-source/django-sb-codefield/-/wikis)
- [Wiki](https://gitlab.com/softbutterfly/open-source/django-sb-codefield/-/wikis)

## Changelog

All changes to versions of this library are listed in the [change history](CHANGELOG.md).

## Development

Check out our [contribution guide](CONTRIBUTING.md).

## Contributors

See the list of contributors [here](https://gitlab.com/softbutterfly/open-source/django-sb-codefield/-/graphs/develop).
