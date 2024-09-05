from fastapi import FastAPI
from starlette.middleware.exceptions import ExceptionMiddleware


class MiddlewareRegistry:

    def __init__(self, app: FastAPI):
        self.app = app

    def register_exception_middleware(self):
        self.app.add_middleware(ExceptionMiddleware, handlers=self.app.exception_handlers)
