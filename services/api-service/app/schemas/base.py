from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(
            validation_alias=to_camel, serialization_alias=to_camel
        ),
        populate_by_name=True,
    )


class Message(BaseModel):
    message: str
