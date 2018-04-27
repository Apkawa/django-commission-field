from django.apps import AppConfig as BaseConfig
from django.utils.translation import ugettext_lazy as _


class CommissionFieldConfig(BaseConfig):
    name = 'commission_field'
    verbose_name = _('Commission Field')
