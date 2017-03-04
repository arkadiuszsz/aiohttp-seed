def middleware_apispec_route(route, router, apispec=None, **kwargs):
    if apispec:
        prefix = apispec.options.get('basePath')
        info = route.resource.get_info()
        if not (info.get('formatter') or info.get('path')).startswith(prefix):
            route.resource.add_prefix(prefix)
        apispec.add_path(route=route)
    return route
