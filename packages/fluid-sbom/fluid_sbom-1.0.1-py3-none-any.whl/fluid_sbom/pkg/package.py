from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
from fluid_sbom.utils.file import (
    Digest,
)
import hashlib
import json
from pydantic import (
    BaseModel,
    Field,
)


@dataclass
class Advisory:  # pylint:disable=too-many-instance-attributes
    cpes: list[str]
    description: str
    epss: float
    id: str  # pylint: disable=invalid-name
    namespace: str
    percentile: float
    severity: str
    urls: list[str]
    version_constraint: str


class Artifact(BaseModel):
    url: str = Field(min_length=1)
    integrity: Digest | None = None


class HealthMetadata(BaseModel):
    latest_version: str | None = Field(default=None, min_length=1)
    latest_version_created_at: str | datetime | None = None
    artifact: Artifact | None = None
    authors: str | None = Field(default=None, min_length=1)


class Package(BaseModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    language: Language
    licenses: list[str]
    locations: list[Location]
    type: PackageType
    advisories: list[Advisory] | None = None
    dependencies: list["Package"] | None = None
    found_by: str | None = Field(default=None, min_length=1)
    health_metadata: HealthMetadata | None = None
    is_dev: bool = False
    metadata: object | None = None
    p_url: str | None = Field(default=None, min_length=1)

    @property
    def id_(self) -> str:
        return self.id_by_hash()

    def id_by_hash(self) -> str:
        try:
            obj_data = {
                "name": self.name,
                "version": self.version,
                "language": self.language.value,
                "type": self.type.value,
                "p_url": self.p_url,
            }
            obj_str = json.dumps(obj_data, sort_keys=True)
            hash_value = hashlib.sha256(obj_str.encode()).hexdigest()
            return hash_value
        except Exception as exc:  # pylint:disable=broad-exception-caught
            return f"could not build ID for object={self}: {exc}"
