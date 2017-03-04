import functools
import marshmallow
from aiohttp import hdrs, web
from apispec.ext.marshmallow.swagger import schema2parameters


def get_schema_data(schema, arguments):
    data = dict()
    for field_name, field_obj in schema.fields.items():
        if not field_obj.required and field_name not in arguments:
            data[field_name] = field_obj.default
            continue
        if field_name not in arguments:
            continue
        if isinstance(field_obj, marshmallow.fields.List) \
                or (isinstance(field_obj, marshmallow.fields.Nested) and field_obj.many is True):
            data[field_name] = arguments[field_name]
        else:
            if isinstance(arguments[field_name], list):  # For tornado url parse results
                data[field_name] = arguments[field_name].pop(0)
            else:
                data[field_name] = arguments[field_name]
    return data


def text_error_response(data, **kwargs):
    text = "\n".join(tuple(
        ' * %s: `%s`' % (
            key,
            '`, `'.join(values)
        ) for key, values in data.items()
    ))
    return web.Response(text=text, **kwargs)


def query_schema(serializer, default_in='formData'):
    def _(method):
        """Validate request body through schema
        and fill parameters info fot apispec module
        :param method: aiohttp handler method
        :return: aiohttp handler method
        """
        parameters = None
        if default_in in ('query', 'formData'):
            parameters = schema2parameters(serializer, default_in=default_in)
        elif default_in == 'body':
            parameters = [{
                'name': 'data',
                'in': 'body',
                'schema': serializer.__class__.__name__.strip('Schema'),
            }]
        if parameters:
            method.apispec = dict(
                parameters=parameters,
                **getattr(method, 'apispec', dict()),
            )

        @functools.wraps(method)
        async def wrapper(self):
            if self.request.headers.get(hdrs.CONTENT_TYPE) == 'application/json':
                self.request.arguments = await self.request.json()
            else:
                self.request.arguments = await self.request.post()

            error_response = text_error_response

            if self.request.headers.get(hdrs.ACCEPT) == 'application/json':
                error_response = web.json_response

            self.request.arguments, errors = serializer.load(
                get_schema_data(
                    serializer,
                    self.request.arguments
                )
            )

            if errors:
                return error_response(
                    data=errors, reason='Bad arguments', status=400)

            return await method(self)
        return wrapper
    return _


def response_schema(serializer):
    pass
