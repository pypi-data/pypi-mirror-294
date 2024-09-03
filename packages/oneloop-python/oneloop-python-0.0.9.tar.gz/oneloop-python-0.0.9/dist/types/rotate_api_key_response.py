# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .rotate_api_key_response_api_key import RotateApiKeyResponseApiKey
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class RotateApiKeyResponse(UniversalBaseModel):
    api_key: RotateApiKeyResponseApiKey = pydantic.Field(alias="apiKey")

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
            extra="allow", frozen=True
        )  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
