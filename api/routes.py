from core.app import app

from api.handlers.specs import SpecsView
from api.handlers.auth import AuthView
from api.specs import spec


app.router.add_route('*', '/specs', SpecsView, apispec=spec)

(
    app.router
    .add_route('*', '/auth/{some}', AuthView, apispec=spec)
    .add_route('*', '/specs', SpecsView, apispec=spec)
    .add_route('*', '/auth/{foo}/', AuthView, apispec=spec)
)
