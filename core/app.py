from aiohttp import web

from core.helpers.loader import import_modules
from core.router import Router
import core.settings as settings


app = web.Application(
    router=Router(
        middlewares=import_modules(settings.route_middlewares)),
    middlewares=import_modules(settings.middlewares),
)
loop = app.loop
