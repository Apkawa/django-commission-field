# coding: utf-8
from __future__ import unicode_literals

from abc import ABC
from decimal import Decimal

from commission_field.db.fields import CommissionTypeEnum


def normalize_decimal(value):
    return Decimal(value).quantize(Decimal('1.00'))


class BaseStrategy(ABC):
    proxy_attrs = [
        'is_percent',
        'is_fixed',
        'value',
        'type',
    ]

    def __init__(self, commission_object):
        """
        :param commission_object:  instance of fields.Commission
        """
        self.obj = commission_object
        self.instance = self.obj.instance

        self._field = commission_object.field
        self._field_name = self._field.name
        self.type_choices = self._field.type_choices
        self.value_field_name = self._field.field_value_name
        self.type_field_name = self._field.field_type_name

    @staticmethod
    def get_percent(total, value):
        return normalize_decimal(Decimal(total) * Decimal((float(value or 0) / 100.0)))

    @staticmethod
    def extract_percent(total_with_percent, percent_value):
        total_with_percent = Decimal(total_with_percent)
        percent = float((percent_value or 0) / 100.0)
        return normalize_decimal(total_with_percent - (total_with_percent / (1 + percent)))

    def is_percent(self):
        return self.type == CommissionTypeEnum.PERCENT

    def is_fixed(self):
        return self.type == CommissionTypeEnum.FIXED

    @classmethod
    def get_property_attrs(cls):
        attrs = {}
        for attr_name in cls.proxy_attrs:
            attr_value = getattr(cls, attr_name)
            if isinstance(attr_value, property):
                attrs[attr_name] = attr_value
        return attrs

    def get_attrs(self):
        attrs = {}
        for attr_name in self.proxy_attrs:
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, property):
                continue
            attrs[attr_name] = attr_value
        return attrs

    def get_value(self):
        return getattr(self.instance, self.value_field_name)

    def set_value(self, value):
        setattr(self.instance, self.value_field_name, value)

    value = property(get_value, set_value)

    def get_type(self):
        return getattr(self.instance, self.type_field_name)

    def set_type(self, value):
        setattr(self.instance, self.type_field_name, value)

    type = property(get_type, set_type)


class GenericStrategy(BaseStrategy):
    pass


class GenericTaxStrategy(BaseStrategy):
    proxy_attrs = BaseStrategy.proxy_attrs + [
        'calculate_tax',
        'extract_tax',
        'update_tax',
        'tax'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tax_field_name = self._field.field_tax_name

    def calculate_tax(self, total):
        if self.is_percent():
            return self.get_percent(total, self.value)

        elif self.is_fixed():
            return normalize_decimal(self.value)
        raise NotImplementedError("Commission type %s not implemented" % self.type)

    def extract_tax(self, total_with_tax):
        '''
        Получаем коммиссию из цены с примененной коммиссией.
        Не учитывает изменения коммиссии

        :param total_with_tax: Стоимость с комиссией
        :return:
        '''
        if self.is_percent():
            return self.extract_percent(total_with_tax, self.value)

        elif self.is_fixed():
            return normalize_decimal(self.value)
        raise NotImplementedError("Commission type %s not implemented" % self.type)

    def update_tax(self, total):
        self.obj.tax = self.calculate_tax(total)

    def get_tax(self):
        if self.tax_field_name is None:
            return
        return getattr(self.instance, self.tax_field_name)

    def set_tax(self, value):
        if self.tax_field_name is None:
            return

        setattr(self.instance, self.tax_field_name, value)

    tax = property(get_tax, set_tax)
