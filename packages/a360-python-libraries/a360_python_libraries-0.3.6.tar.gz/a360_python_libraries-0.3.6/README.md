# a360-python-libraries

Python shared libraries for a360 applications

## Preparation

### Prepare GitHub access

To have access to Docker images registry on GitHub, you should create an access token at [GitHub profile settings / Developer tools / Access tokens](https://github.com/settings/tokens) with permission `read:packages`

After that, put your GitHub username and token into `.env` file at project root directory:

```dotenv
GITHUB_USER=username
GITHUB_TOKEN=token
```

### Login to your GitHub registry

```bash
make login
```

## Add package into your project

Add the following line into your `pyproject.toml` file:

```toml
a360-python-libraries = { git = "git@github.com:aesthetics-360/a360-python-libraries.git", tag = "0.2.0" }
```

and run:

```bash
make build
```

## Usage

### Role based access control

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_role
from a360_security.enums import Role

router = APIRouter()

@router.get(
    ...,
    dependencies=[Depends(require_role(Role.ADMIN))]
)
def get() -> dict:
    ...
```


### User dependency

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_user
from a360_security.dto import UserDTO

router = APIRouter()

@router.get(
    ...,
)
def get(user: UserDTO = Depends(require_user)) -> dict:
    ...
```


### Client platform

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_client_platform
from a360_security.enums import ClientPlatform

router = APIRouter()

@router.get(
    ...,
)
def get(client_platform: ClientPlatform = Depends(require_client_platform)) -> dict:
    ...
```