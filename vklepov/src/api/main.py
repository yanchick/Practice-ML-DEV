"""FastAPI router module."""
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from . import router, users

app = FastAPI()

app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.include_router(users.user_router)
app.include_router(router.router, prefix="/api")
