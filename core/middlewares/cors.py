from aiohttp import hdrs, web


async def middleware_cors(app, handler):
    access_control_allow_headers = ', '.join((
        hdrs.ORIGIN, hdrs.CONTENT_TYPE, hdrs.ACCEPT, hdrs.AUTHORIZATION, hdrs.WWW_AUTHENTICATE))
    access_control_methods = ', '.join((method for method in hdrs.METH_ALL if hasattr(handler, method.lower())))

    async def middleware_handler(request):
        if request.method == hdrs.METH_OPTIONS:
            response = web.Response()
        else:
            response = await handler(request)
        response.headers.update({
            hdrs.ACCESS_CONTROL_ALLOW_ORIGIN: request.headers.get(hdrs.ORIGIN, '*'),
            hdrs.ACCESS_CONTROL_ALLOW_HEADERS: access_control_allow_headers,
            hdrs.ACCESS_CONTROL_ALLOW_METHODS: access_control_methods,
            hdrs.ACCESS_CONTROL_ALLOW_CREDENTIALS: 'true',
        })
        return response
    return middleware_handler
