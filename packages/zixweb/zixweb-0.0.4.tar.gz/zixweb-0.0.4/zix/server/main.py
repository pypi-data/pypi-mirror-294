import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import database, logging, utils


LOGGER = logging.get_logger(logger_name=__name__)

# dynamic imports from external directries
CURRENT_DIR =  os.path.join(os.getcwd())
config = utils.dynamic_import(CURRENT_DIR, "config")
plugins = utils.import_submodules(CURRENT_DIR, "plugins")

# Initialize the FastAPI app
app = FastAPI(
        middleware=config.MIDDLEWARE,
        docs_url=config.DOCS_URL,
        redoc_url=config.REDOC_URL,
        )

if config.DATABASE_URL:
    engine = database.get_engine(
        config.DATABASE_URL,
        config.DB_CONNECT_ARGS,
        config.DB_ENGINE_KWARGS,
        )


# Register plugin routers
plugin_modules = utils.list_submodules(plugins)
for module_name in plugin_modules.keys():
    LOGGER.info(f"Plugin {module_name} has been registered.")
    router = getattr(plugin_modules[module_name], "router")
    app.include_router(router)
    LOGGER.debug(f"Registered router: {module_name}")

# Mount static files. You should replace the static file path with CDN in production.
app.mount(
    "/assets",
    StaticFiles(directory=config.STATIC_DIR + "/assets"),
    name="static",
)
LOGGER.info(f"Mounted /assets to {config.STATIC_DIR}/assets")


# Mount static files. You should replace the static file path with CDN in production.
app.mount(
    "/",
    StaticFiles(directory=config.STATIC_DIR, html=True),
    name="static",
)
LOGGER.info(f"Mounted / to {config.STATIC_DIR}")
