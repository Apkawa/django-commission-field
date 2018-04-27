from django.db import models

from commission_field.db.fields import CommissionField


class Example(models.Model):
    discount = CommissionField()


