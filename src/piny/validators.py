from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from .errors import ValidationError

LoadedData = Union[Dict[str, Any], List[Any]]


class Validator(ABC):
    """
    Abstract base class for optional validator classes

    Use only to derive new child classes, implement all abstract methods
    """

    def __init__(self, schema: Any, **params):
        self.schema = schema
        self.schema_params = params

    @abstractmethod
    def load(self, data: LoadedData, **params):
        """
        Load data, return validated data or raise en error
        """
        pass  # pragma: no cover


class PydanticValidator(Validator):  # pragma: no cover
    """
    Validator class for Pydantic Version 1
    """

    def load(self, data: LoadedData, **params):
        try:
            return self.schema(**data).dict()
        except Exception as e:
            raise ValidationError(origin=e, reason=str(e))


class PydanticV2Validator(Validator):
    """
    Validator class for Pydantic Version 2
    """

    def load(self, data: LoadedData, **params):
        try:
            return self.schema(**data).model_dump()
        except Exception as e:
            raise ValidationError(origin=e, reason=str(e))


class MarshmallowValidator(Validator):
    """
    Validator class for Marshmallow library
    """

    def load(self, data: LoadedData, **params):
        try:
            return self.schema(**self.schema_params).load(data, **params)
        except Exception as e:
            raise ValidationError(origin=e, reason=str(e))


class TrafaretValidator(Validator):
    """
    Validator class for Trafaret library
    """

    def load(self, data: LoadedData, **params):
        try:
            return self.schema.check(data)
        except Exception as e:
            raise ValidationError(origin=e, reason=str(e))
