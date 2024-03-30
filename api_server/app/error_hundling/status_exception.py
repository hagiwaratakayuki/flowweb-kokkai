
from fastapi.responses import Response
from .binder import exception_binder

class StatusException(Exception):
    def __init__(self, status:int, *args: object) -> None:
        
        self.status = status
        super().__init__(*args)

async def exception_handler(request, exception:StatusException):
    return Response(
        status_code=exception.status
    )
    
binder = exception_binder(StatusException, exception_handler)        

