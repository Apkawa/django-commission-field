# -*- coding: utf-8 -*-

from commission_field.db.fields import CommissionField, CommissionTypeEnum
from tests.models import Example


def test_example():
    example = Example()
    assert example.discount.value == 0
    assert example.discount_value == 0
    assert example.discount.type == CommissionTypeEnum.PERCENT
    assert example.discount_type == CommissionTypeEnum.PERCENT
    example.discount.value = 100
    assert example.discount.value == 100
    assert example.discount_value == 100
