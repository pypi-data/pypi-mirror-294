from typing import Any

from pydantic import BaseModel

from earthscale import DatasetDomain
from earthscale.datasets.dataset import DatasetMetadata, DatasetType


class DatasetRegistrationRequest(BaseModel):
    id: str
    name: str
    metadata: DatasetMetadata
    type: DatasetType
    domain: DatasetDomain
    class_name: str
    dataset_definition: dict[str, Any]
