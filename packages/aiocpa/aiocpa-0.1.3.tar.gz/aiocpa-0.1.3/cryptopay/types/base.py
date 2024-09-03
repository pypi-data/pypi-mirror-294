from abc import ABC
from typing import TYPE_CHECKING, Annotated, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, PrivateAttr
from pydantic.functional_serializers import PlainSerializer

from cryptopay.utils import serialize_list

if TYPE_CHECKING:
    from cryptopay import CryptoPay

CryptoPayType = TypeVar("CryptoPayType", bound="CryptoPayObject | list | bool")
T = TypeVar("T")
SerList = Annotated[list[T], PlainSerializer(serialize_list, str)]


class CryptoPayObject(BaseModel, ABC):
    """Base object class for types."""

    _client: "CryptoPay" = PrivateAttr()

    model_config = ConfigDict(
        extra="allow",
    )

    def model_post_init(self, ctx: dict) -> None:
        """Bind client to CryptoPayObject."""
        self._client = ctx["client"]


class Error(BaseModel):
    """API error model."""

    code: int
    name: str

    model_config = ConfigDict(
        extra="allow",
        frozen=True,
    )


class ItemsList(BaseModel, Generic[CryptoPayType]):
    """
    Items list.

    This model is used to convert a dictionary with the `items` key to a list.
    """

    items: CryptoPayType


class Response(BaseModel, Generic[CryptoPayType]):
    """API response model."""

    ok: bool
    result: CryptoPayType | ItemsList[CryptoPayType] | None = None
    error: Error | None = None
