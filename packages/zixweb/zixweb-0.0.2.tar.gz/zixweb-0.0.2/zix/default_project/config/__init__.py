import os

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
# from starlette.middleware.authentication import AuthenticationMiddleware
# from starlette_context import plugins
# from starlette_context.middleware import RawContextMiddleware

from zix.server import utils
from .common import *


if utils.is_local():
    from .local import *
else:
    from .server import *


MIDDLEWARE= [
    Middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(
        SessionMiddleware,
        secret_key=SECRET_KEY,
    ),
    # Middleware(
    #     RawContextMiddleware,
    #     plugins=(
    #         plugins.RequestIdPlugin(),
    #         plugins.CorrelationIdPlugin()
    #     ),
    # ),
]

if USE_AUTH0:
    from zix.server import auth0
    MIDDLEWARE.append(Middleware(
        AuthenticationMiddleware,
        backend=OpenIDAuthBackend(),
        )
    )
