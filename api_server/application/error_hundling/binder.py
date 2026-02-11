from fastapi import FastAPI

def exception_binder(exception_type, hundler):
    def binder(app:FastAPI):
        return app.exception_handler(exception_type)(hundler)
    return binder