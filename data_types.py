import typing
import pydantic

# Byte
Byte = typing.Annotated[int, pydantic.Field(ge=0x00, le=0xFF)]
