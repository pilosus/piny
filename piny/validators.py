from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from .errors import ValidationError

LoadedData = Union[Dict[str, Any], List[Any]]


class Validator(ABC):
    def __init__(self, schema: Any, **params):
        self.schema = schema
        self.schema_params = params

    @abstractmethod
    def load(self, data: LoadedData, **params):
        """
        Load data, return validated data or raise en error
        """
        pass  # pragma: no cover


class PydanticValidator(Validator):
    def load(self, data: LoadedData, **params):
        try:
            return self.schema(**data).dict()
        except Exception as e:
            raise ValidationError(origin=e, reason=str(e))


class MarshmallowValidator(Validator):
    def load(self, data: LoadedData, **params):
        try:
            return self.schema(**self.schema_params).load(data, **params).data
        except Exception as e:
            raise ValidationError(origin=e, reason=str(e))


class TrafaretValidator(Validator):
    def load(self, data: LoadedData, **params):
        try:
            return self.schema.check(data)
        except Exception as e:
            raise ValidationError(origin=e, reason=str(e))
