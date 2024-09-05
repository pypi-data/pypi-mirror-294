from _typeshed import Incomplete
from amsdal.cloud.constants import JWT_PUBLIC_KEY as JWT_PUBLIC_KEY
from amsdal.cloud.services.auth.base import AuthHandlerBase as AuthHandlerBase
from amsdal.errors import AmsdalAuthenticationError as AmsdalAuthenticationError
from amsdal.schemas.manager import SchemaManager as SchemaManager

HMAC_KEY: bytes

class TokenAuthHandler(AuthHandlerBase):
    __token: Incomplete
    public_key: Incomplete
    def __init__(self, token: str | None, public_key: str = ...) -> None: ...
    def _validate_checksum(self, expected_checksum: str) -> None: ...
    def validate_credentials(self) -> None: ...
