import pydantic


class Byte(pydantic.BaseModel):
    value: int

    @classmethod
    @pydantic.field_validator("value")
    def value_validator(cls, value: int) -> int:
        return value & 0xFF
