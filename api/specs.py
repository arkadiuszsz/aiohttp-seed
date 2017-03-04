from apispec import APISpec
from api.helpers.specs import yaml_serializer


spec = APISpec(
    title='Async Python project',
    version='1.0.0',
    info=dict(
        description='A minimal API example'
    ),
    plugins=[
        'apispec.ext.marshmallow',
        'plugins.apispec.aiohttp',
    ],
    basePath='/api/v1',
)

spec.register_path_helper(yaml_serializer)
