from typing import List
from typing import Optional

from server.utils import http_status


class APIException(Exception):
    status_code = http_status.HTTP_400_BAD_REQUEST

    def __init__(self, payload: List[str], status_code: Optional[int] = None):
        super().__init__()
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


class BadRequest(APIException):
    status_code = http_status.HTTP_400_BAD_REQUEST

class ServerError(APIException):
    status_code = http_status.HTTP_500_INTERNAL_SERVER_ERROR
