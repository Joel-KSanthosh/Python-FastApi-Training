from fastapi import HTTPException


class EmailAlreadyExistsError(HTTPException):
    pass


class UserWithGivenIdDoesntExist(HTTPException):
    pass
