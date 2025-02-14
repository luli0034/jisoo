from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Any
from jisoo.models.input import JSONPath
from jisoo.utils import replace_keys_with_prefix, process_context
from enum import Enum


class CommonObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_dict(self):
        return {
            k: v
            for k, v in (
                process_context(k, v)
                for k, v in self.model_dump().items()
                if v is not None
            )
        }

    def to_pascalcase(self, text):
        return "".join([t.title() for t in text.split("_")])


class KeyValuePair(CommonObject):
    """Represents a key-value pair for environment variables."""

    name: str
    value: str | JSONPath


class EnvironmentFile(CommonObject):
    """Represents an environment file containing environment variables."""

    type: str = Field("s3", description="The type of environment file", frozen=True)
    value: str  # The S3 URI of the file containing environment variables


class ResourceRequirement(CommonObject):
    """Represents the resource requirements for a container."""

    type: Literal["GPU", "InferenceAccelerator"]
    value: str  # The amount of the resource


class BaseErrors(str, Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return repr(self.value)
