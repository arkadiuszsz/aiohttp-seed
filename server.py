import os
from aiohttp import web
from core.app import app
from core.helpers.loader import load


load('routes')

web.run_app(
    app,
    host=os.environ.get('HOST', '127.0.0.1'),
    port=int(os.environ.get('PORT', '8000')),
)
