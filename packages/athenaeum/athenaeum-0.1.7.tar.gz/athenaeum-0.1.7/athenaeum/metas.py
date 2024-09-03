def merge_metastases(*meta: type, name: str = '_') -> type:
    return type(name, meta, {})


class BasesAttrsMergeMeta(type):
    def __new__(mcs, name, bases, attrs):
        temp_attrs = dict()
        for base in bases:
            for base_attr_name, base_attr_value in base.__dict__.items():
                if base_attr_name not in temp_attrs:
                    if not base_attr_name.startswith('__') and not base_attr_name.endswith('__'):
                        temp_attrs[base_attr_name] = base_attr_value
        temp_attrs.update(attrs)
        attrs = temp_attrs
        return super().__new__(mcs, name, bases, attrs)
