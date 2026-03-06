from contextlib import asynccontextmanager
from fastapi import FastAPI

from notification_service.container import container
from notification_service.routers import notifications


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo = container.mongo
    
    await container.notification_repo.ensure_indexes()

    app.state.mongo = mongo

    yield

    await mongo.close()


def include_all_routes(app):
    app.include_router(notifications.router)


# Application startup
app = FastAPI(lifespan=lifespan)
include_all_routes(app)
