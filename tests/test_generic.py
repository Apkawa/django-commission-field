# -*- coding: utf-8 -*-

from commission_field.db.fields import CommissionTypeEnum
from tests.models import Example


def test_example():
    example = Example()
    assert example.discount.value == 0
    assert example.discount_value == 0
    assert example.discount.type == CommissionTypeEnum.PERCENT.value
    assert example.discount_type == CommissionTypeEnum.PERCENT.value
    example.discount.value = 100
    assert example.discount.value == 100
    assert example.discount_value == 100


def test_set_value():
    example = Example()
    example.discount = 10
    assert example.discount.value == 10


def test_create():
    example = Example.objects.create(discount=10)
    assert example.discount.value == 10


def test_functions():
    example = Example.objects.create(discount=10)
    assert example.discount.is_percent()


def test_calculation():
    example = Example.objects.create(discount_value=10, discount_type=CommissionTypeEnum.PERCENT.value)
    assert example.discount.calculate_tax(1000) == 100.
