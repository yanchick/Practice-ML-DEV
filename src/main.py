from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.routes import routers as v1_routers
from core.config import configs
from core.container import Container
from util.class_object import singleton
from core.database import init_db

#init_db()

@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
            debug=configs.DEBUG
        )

        # set db and container
        self.container = Container()
        self.db = self.container.db()
        self.db.create_database()

        # set cors
        if configs.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)

    def create_tables(self):
        # Create tables using SQLAlchemy's create_all
        self.db.create_all()


app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
container = app_creator.container

from celery import Celery
from celery_config import CELERY_BROKER_URL

celery = Celery('tasks', broker=CELERY_BROKER_URL)

celery.autodiscover_tasks(['tasks'])
