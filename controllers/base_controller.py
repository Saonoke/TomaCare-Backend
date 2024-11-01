from fastapi import HTTPException
from starlette import status

class BaseController:
    def ise(self, e: Exception):
        # log exception into file
        print(e)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong in our end !")
