from aiohttp.web import DynamicResource, PlainResource


def middleware_linkedroute(route, router, **settings):
    def add_route(method, path, handler, **kwargs):
        if isinstance(route.resource, DynamicResource):
            path = route.get_info()['formatter'] + path
        if isinstance(route.resource, PlainResource):
            path = route.get_info()['path'] + path
        kwargs.update(settings)
        return router.add_route(method, path, handler, **kwargs)

    route.add_route = add_route
    return route
