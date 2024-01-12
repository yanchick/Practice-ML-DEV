""" A client library for accessing FastAPI """
from .api import model, prediction, user
from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
    "user",
    "prediction",
    "model",
)
