import os
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


BASE_DIR = os.getcwd()


middlewares = (
    'core.middlewares.cors.middleware_cors',
)

route_middlewares = (
    'core.middlewares.route.middleware_linkedroute',
    'api.middlewares.spec.middleware_apispec_route',
)
