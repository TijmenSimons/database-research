import random
from typing import TypedDict
import enum


class Field(TypedDict):
    type: str
    required: bool
    properties: list["Field"] | None


class Types(str, enum.Enum):
    STRING = "string"
    OBJECT = "object"
    # ARRAY = "array"
    INTEGER = "integer"
    BOOLEAN = "boolean"


class MongoActions:
    @staticmethod
    def create_field() -> Field:
        type = random.choice([i.value for i in Types])
        properties = None

        if type == "object":
            properties = [MongoActions.create_field() for _ in range(random.choice([1, 2, 3]))]

        return {
            "type": type,
            "required": random.choice([True, False]),
            "properties": properties
        }

