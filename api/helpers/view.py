import asyncio
from aiohttp import web


class JsonView(web.View):

    @asyncio.coroutine
    def __iter__(self):
        response = (yield from super().__iter__())
        if isinstance(response, web.Response):
            return response
        return web.json_response(response)
