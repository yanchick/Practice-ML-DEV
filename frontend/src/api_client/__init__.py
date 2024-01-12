""" A client library for accessing FastAPI """
from . import models
from .api import model, prediction, user
from .client import AuthenticatedClient, Client

__all__ = ("AuthenticatedClient", "Client", "user", "prediction", "model", "models")
