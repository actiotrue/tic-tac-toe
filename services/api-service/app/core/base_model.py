from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import Any, Optional, TypeVar, Union, get_args, get_origin, get_type_hints

from asyncpg import Record

T = TypeVar("T", bound="DBModel")


@dataclass(slots=True)
class DBModel:
    @classmethod
    def from_row(cls: type[T], row: Union[Record, None]) -> Optional[T]:
        if row is None:
            return None

        hints = get_type_hints(cls)
        data = {}
        for field in fields(cls):
            if field.name not in row:
                if field.default is not field.default_factory:
                    continue
                raise ValueError(f"Missing field: {field.name} in model {cls.__name__}")
            field_name = field.name
            field_type = hints[field_name]
            value = row[field_name]

            origin = get_origin(field_type)
            args = get_args(field_type)

            is_nullable = (origin is Union or origin is Optional) and type(None) in args
            target_type = (
                next((a for a in args if a is not type(None)), field_type)
                if is_nullable
                else field_type
            )

            if value is None:
                if is_nullable or field.default is not field.default_factory:
                    data[field_name] = None
                    continue
                raise ValueError(f"Field {field.name} is NULL but not Optional")

            # 1:M
            if origin is list:
                item_type = args[0]
                if is_dataclass(item_type) and hasattr(item_type, "from_row"):
                    data[field_name] = [item_type.from_row(item) for item in value]
                else:
                    data[field_name] = value
            # 1:1
            elif is_dataclass(target_type) and hasattr(target_type, "from_row"):
                data[field_name] = target_type.from_row(value)
            # Base field
            else:
                data[field_name] = value
        return cls(**data)

    @classmethod
    def from_rows(cls: type[T], rows: list[Record]) -> list[T]:
        return [cls.from_row(row) for row in rows]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
