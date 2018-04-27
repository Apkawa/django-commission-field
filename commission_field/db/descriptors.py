import six


class CommissionMeta(type):
    def __new__(mcls, name, bases, attrs):
        new_cls = type(name, bases, attrs)
        return new_cls


@six.add_metaclass(CommissionMeta)
class Commission(object):

    def __init__(self, instance, field):
        self.instance = instance
        self.field = field

        self.field_name = field.name

        strategy_class = field.get_strategy_class()
        strategy = strategy_class(self)
        property_attrs = strategy_class.get_property_attrs()
        for name, value in property_attrs.items():
            _prop = {'fget': value.fget, 'fset': value.fset, 'fdel': value.fdel}
            for k, v in list(_prop.items()):
                if v is None:
                    continue
                _prop[k] = (lambda prop_v: lambda self, *args, **kwargs: prop_v(strategy, *args, **kwargs))(v)
            setattr(self.__class__, name, property(**_prop))

        attrs = strategy.get_attrs()
        for name, value in attrs.items():
            setattr(instance, name, value)

    def __repr__(self):
        return '<value: {self.value}, type: {self.type}, tax:{self.tax}>'.format(self=self)


class CommissionDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError('Can only be accessed via an instance.')
        return Commission(instance=instance, field=self.field)

    def __set__(self, obj, value):
        if isinstance(value, Commission):
            setattr(obj, self.field.value_field_name, value.value)
            setattr(obj, self.field.type_field_name, value.type)
        else:
            setattr(obj, self.field.value_field_name, value)
            # raise AttributeError("Value should be Commission object. May be mean .value|.tax|.type?")
