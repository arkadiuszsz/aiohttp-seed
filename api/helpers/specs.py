def yaml_serializer(view, **kwargs):
    def replace_nums(d):
        for k, v in d.items():
            if isinstance(k, int):
                d[str(k)] = v
                del d[k]
            if isinstance(v, dict):
                replace_nums(v)

    def add_schema_ref(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, dict):
                    add_schema_ref(v)
                elif isinstance(v, list):
                    list(map(add_schema_ref, v))
                elif k in ('schema', 'items'):
                    d[k] = {'$ref': '#/definitions/' + v.strip('Schema')}

    replace_nums(kwargs['path'])
    add_schema_ref(kwargs['path'])
    return kwargs['path']


def definition(spec, **kwargs):
    def wrapper(schema):
        spec.definition(
            schema.__name__.strip('Schema'),
            schema=schema,
            **kwargs
        )
        return schema
    return wrapper
