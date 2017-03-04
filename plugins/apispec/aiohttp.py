from aiohttp.web import ResourceRoute, DynamicResource, PlainResource

from apispec import Path
from apispec import utils
from apispec.exceptions import APISpecError


def setup(spec):
    """Setup for the plugins."""
    spec.register_path_helper(path_from_urlspec)


def path_from_urlspec(spec, route, operations, **kwargs):
    if not isinstance(route, ResourceRoute):
        raise Exception('Route is not ResourceRoute instance %s' % type(route))

    extensions = extensions_from_handler(route.handler)

    if operations is None:
        operations = {}
        for operation in operations_from_methods(route.handler, extensions):
            operations.update(operation)
        if not operations:
            raise APISpecError(
                'Could not find endpoint for route {0}'.format(route))

    if isinstance(route.resource, DynamicResource):
        path = route.get_info()['formatter']

    if isinstance(route.resource, PlainResource):
        path = route.get_info()['path']

    return Path(path=path, operations=operations)


def operations_from_methods(handler, extensions):
    """Generator of operations described in handler's http methods
    :param handler:
    """
    for httpmethod in utils.PATH_KEYS:
        method = getattr(handler, httpmethod, None)
        if method is None:
            continue
        operation_data = dict()
        operation_data.update(extensions)
        operation_data.update(getattr(method, 'apispec', dict()))
        operation_data.update(utils.load_yaml_from_docstring(method.__doc__) or {})
        if operation_data:
            operation = {httpmethod: operation_data}
            yield operation


def extensions_from_handler(handler):
    """Returns extensions dict from handler docstring
    :param handler:
    """
    extensions = utils.load_yaml_from_docstring(handler.__doc__) or {}
    return extensions
