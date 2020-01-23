import enum
from decimal import Decimal

import six
from django.db import models

from commission_field.db.descriptors import Commission, CommissionDescriptor

try:
    from django.utils.module_loading import import_string
except ImportError:
    from django.utils.module_loading import import_by_path as import_string

_commission_type_field_name = lambda name: '%s_type' % name
_commission_value_field_name = lambda name: '%s_value' % name
_commission_tax_field_name = lambda name: '%s_tax' % name


class CommissionTypeEnum(enum.Enum):
    PERCENT = 0
    FIXED = 1


COMMISSION_TYPE_CHOICES = [
    [CommissionTypeEnum.PERCENT.value, 'Процентный'],
    [CommissionTypeEnum.FIXED.value, 'Фиксированный'],
]

DEFAULT_STRATEGY_CLASS = 'commission_field.strategy.GenericStrategy'


class CommissionField(models.Field):
    def __init__(self, verbose_name=None, name=None,
                 type_choices=COMMISSION_TYPE_CHOICES,
                 type_default=CommissionTypeEnum.PERCENT.value,
                 tax_default=Decimal(0),
                 value_default=Decimal(0),
                 **kwargs):
        kwargs.setdefault('strategy_class', DEFAULT_STRATEGY_CLASS)
        self.type_choices = type_choices
        self.type_default = type_default
        self.tax_default = tax_default
        self.value_default = value_default
        self.strategy_class = kwargs.pop('strategy_class', None)
        super(CommissionField, self).__init__(verbose_name, name, **kwargs)

    def get_strategy_class(self):
        if isinstance(self.strategy_class, six.string_types):
            return import_string(self.strategy_class)
        return self.strategy_class

    def add_fields(self, cls, name):
        self.field_type_name = _commission_type_field_name(name)
        self.field_value_name = _commission_value_field_name(name)

        # TODO handle enum value
        commission_type_field = models.PositiveSmallIntegerField(
            'Тип комисcии',
            default=self.type_default,
            choices=self.type_choices,
            null=False if self.type_default else True,
            blank=False if self.type_default else True
        )

        commission_value_field = models.DecimalField(
            'Значение комиссии',
            max_digits=10,
            decimal_places=2,
            default=Decimal('0.0'),
        )
        commission_type_field.creation_counter = self.creation_counter + 1
        commission_value_field.creation_counter = self.creation_counter + 2
        cls.add_to_class(self.field_type_name, commission_type_field)
        cls.add_to_class(self.field_value_name, commission_value_field)

    def contribute_to_class(self, cls, name, **kwargs):
        if not cls._meta.abstract:
            self.add_fields(cls, name)

        super(CommissionField, self).contribute_to_class(cls, name)
        # Do not create column
        self.column = None
        self.concrete = False
        setattr(cls, self.name, CommissionDescriptor(self))

    def get_prep_value(self, value):
        if isinstance(value, Commission):
            return value.value
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        if hasattr(value, 'value'):
            return value.value
        return value

    def to_python(self, value):
        if isinstance(value, Commission):
            return value
        else:
            return super(CommissionField, self).to_python(value)


DEFAULT_TAX_STRATEGY_CLASS = 'commission_field.strategy.GenericTaxStrategy'


class CommissionTaxField(CommissionField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('strategy_class', DEFAULT_STRATEGY_CLASS)

    def add_fields(self, cls, name):
        self.field_tax_name = _commission_tax_field_name(name)
        super().add_fields(cls, name)
        commission_tax_field = models.DecimalField(
            'Комиссия',
            max_digits=10,
            decimal_places=2,
            default=self.tax_default,
            null=False if self.tax_default is not None else True,
            blank=False if self.tax_default is not None else True
        )
        commission_tax_field.creation_counter = self.creation_counter + 3
        cls.add_to_class(self.field_tax_name, commission_tax_field)
