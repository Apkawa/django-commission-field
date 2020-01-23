[![PyPi](https://img.shields.io/pypi/v/django-commission-field.svg)](https://pypi.python.org/pypi/django-commission-field)
[![Build Status](https://travis-ci.org/Apkawa/django-commission-field.svg?branch=master)](https://travis-ci.org/Apkawa/django-commission-field)
[![Documentation Status](https://readthedocs.org/projects/django-commission-field/badge/?version=latest)](https://pytest-ngrok.readthedocs.io/en/latest/?badge=latest)
[![Codecov](https://codecov.io/gh/Apkawa/django-commission-field/branch/master/graph/badge.svg)](https://codecov.io/gh/Apkawa/django-commission-field)
[![Requirements Status](https://requires.io/github/Apkawa/django-commission-field/requirements.svg?branch=master)](https://requires.io/github/Apkawa/django-commission-field/requirements/?branch=master)
[![PyUP](https://pyup.io/repos/github/Apkawa/django-commission-field/shield.svg)](https://pyup.io/repos/github/Apkawa/django-commission-field)
[![PyPi Python versions](https://img.shields.io/pypi/pyversions/django-commission-field.svg)](https://pypi.python.org/pypi/django-commission-field)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# Installation

```bash
pip install django-commission-field
```

or from git

```bash
pip install -e git+https://githib.com/Apkawa/django-commission-field.git@master#egg=django-commission-field
```

## Django and python version

| Python<br/>Django | 3.5 | 3.6 | 3.7 | 3.8 |
|:-----------------:|-----|-----|-----|-----|
| 1.8               |  ✘  |  ✘  |  ✘  |  ✘  |
| 1.11              |  ✔  |  ✔  |  ✔  |  ✘  |
| 2.2               |  ✔  |  ✔  |  ✔  |  ✔  |
| 3.0               |  ✘  |  ✔  |  ✔  |  ✔  |


# Usage

```python
from django.db import models
from commission_field.db.fields import CommissionField, CommissionTypeEnum


class ExampleModel(models.Model):
    discount = CommissionField()


example = ExampleModel(discount_value=10, discount_type=CommissionTypeEnum.PERCENT)
assert example.discount.calculate_tax(1000) == 100
```
