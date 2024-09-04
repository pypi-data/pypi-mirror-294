from abc import ABC

from pydantic import BaseModel

from griff.domain.common_types import EntityId


class ApiOut(BaseModel, ABC):  # pragma: no cover
    ...


class EntityIdOut(ApiOut):  # pragma: no cover11
    entity_id: EntityId
