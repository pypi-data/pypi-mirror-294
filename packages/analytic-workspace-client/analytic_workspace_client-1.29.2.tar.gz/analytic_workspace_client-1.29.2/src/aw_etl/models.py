from typing import Protocol, List, Any


class ModelObjectField(Protocol):
    """ """
    @property
    def simple_type(self) -> str:
        """ """


class ModelObject(Protocol):
    """ """
    @property
    def fields(self) -> List[ModelObjectField]:
        """ """


class Vault(Protocol):
    """ """
    def get(self, name: str) -> Any:
        """ """

