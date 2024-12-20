from fastapi import status

from application.error_hundling.status_exception import StatusException


def exec(response):
    if response == None:
        raise StatusException(status=status.HTTP_404_NOT_FOUND)
