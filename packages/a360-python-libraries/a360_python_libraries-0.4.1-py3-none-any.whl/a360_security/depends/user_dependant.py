from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..utils.aws_cognito import AWSCognitoService, get_aws_cognito
from ..dto import UserDTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def require_user(
        token: str = Depends(oauth2_scheme),
        cognito_service: AWSCognitoService = Depends(get_aws_cognito)
) -> UserDTO:
    return UserDTO(**cognito_service.get_current_user(token))
