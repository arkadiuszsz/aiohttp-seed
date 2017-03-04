from aiohttp.web import UrlDispatcher


class Router(UrlDispatcher):

    def __init__(self, middlewares=None, *args, **kwargs):
        self.middlewares = tuple(middlewares)
        return super().__init__(*args, **kwargs)

    def add_route(self, method, path, handler,
                  *, name=None, expect_handler=None, **kwargs):
        route = super().add_route(method, path, handler, name=None, expect_handler=None)
        for middleware in self.middlewares:
            route = middleware(route, self, **kwargs)
        return route
