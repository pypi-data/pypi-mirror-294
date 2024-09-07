from cyclonedx.exception import (
    MissingOptionalDependencyException,
)
from cyclonedx.factory.license import (
    LicenseFactory,
)
from cyclonedx.model import (
    Tool,
)
from cyclonedx.model.bom import (
    Bom,
)
from cyclonedx.model.component import (
    Component,
    ComponentType,
)
from cyclonedx.model.license import (
    LicenseExpression,
)
from cyclonedx.output import (
    make_outputter,
)
from cyclonedx.output.json import (
    JsonV1Dot5,
)
from cyclonedx.schema import (
    OutputFormat,
    SchemaVersion,
)
from cyclonedx.validation import (
    make_schemabased_validator,
)
from cyclonedx.validation.json import (
    JsonStrictValidator,
)
from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.config.config import (
    SbomConfig,
)
from fluid_sbom.format.common import (
    set_namespace_version,
)
from fluid_sbom.pkg.package import (
    Package,
)
from packageurl import (
    PackageURL,
)
import sys
from typing import (
    cast,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from cyclonedx.output.json import (
        Json as JsonOutputter,
    )
    from cyclonedx.output.xml import (
        Xml as XmlOutputter,
    )
    from cyclonedx.validation.xml import (
        XmlValidator,
    )


def format_cyclone_json(bom: Bom, output: str) -> None:
    json_output: "JsonOutputter" = JsonV1Dot5(bom)
    serialized_json = json_output.output_as_string()
    my_json_validator = JsonStrictValidator(SchemaVersion.V1_5)
    try:
        validation_errors = my_json_validator.validate_str(serialized_json)
        if validation_errors:
            print(
                "warn",
                "JSON invalid",
                "ValidationError:",
                repr(validation_errors),
                sep="\n",
                file=sys.stderr,
            )
        print("info", "CycloneDx JSON valid, generating output file")
        json_output.output_to_file(f"{output}.json", True, indent=2)
    except MissingOptionalDependencyException as error:
        print("error", "CycloneDx JSON-validation was skipped due to", error)


def format_cyclone_xml(bom: Bom, output: str) -> None:
    xml_output: "XmlOutputter" = make_outputter(
        bom, OutputFormat.XML, SchemaVersion.V1_5
    )

    serialized_xml = xml_output.output_as_string()
    my_xml_validator: "XmlValidator" = make_schemabased_validator(
        xml_output.output_format, xml_output.schema_version
    )
    try:
        validation_errors = my_xml_validator.validate_str(serialized_xml)
        if validation_errors:
            print(
                "XML invalid",
                "ValidationError:",
                repr(validation_errors),
                sep="\n",
                file=sys.stderr,
            )
        print("info", "CycloneDx XML valid, generating output file")
        xml_output.output_to_file(f"{output}.xml", True, indent=2)
    except MissingOptionalDependencyException as error:
        print("error", "CycloneDx XML-validation was skipped due to", error)


def pkg_to_component(package: Package) -> Component:
    lc_factory = LicenseFactory()
    licenses = []
    for lic in package.licenses:
        item = lc_factory.make_from_string(lic)
        if not isinstance(item, LicenseExpression):
            licenses.append(item)
    return Component(
        type=ComponentType.LIBRARY,
        name=package.name,
        version=package.version,
        licenses=licenses,
        bom_ref=f"{package.name}@{package.version}",
        purl=PackageURL.from_string(package.p_url) if package.p_url else None,
    )


def format_cyclonedx_sbom(  # pylint:disable=too-many-locals
    packages: list[Package],
    relationships: list[Relationship],
    file_format: str,
    output: str,
    config: SbomConfig,
) -> None:
    namespace, version = set_namespace_version(config=config)
    bom = Bom()
    bom.metadata.component = root_component = Component(
        name=namespace,
        type=ComponentType.APPLICATION,
        licenses=[],
        bom_ref="",
        version=version,
    )
    bom.metadata.tools.add(Tool(vendor="Fluid Attacks", name="Fluid-Sbom"))

    components = [pkg_to_component(package) for package in packages]
    for component in components:
        bom.components.add(component)
        bom.register_dependency(root_component, [component])

    dependency_map: dict[Component, list[Component]] = {}

    for relationship in relationships:
        to_pkg = pkg_to_component(cast(Package, relationship.to_))
        from_pkg = pkg_to_component(cast(Package, relationship.from_))

        if to_pkg not in dependency_map:
            dependency_map[to_pkg] = []

        dependency_map[to_pkg].append(from_pkg)

        for ref, depends_on_list in dependency_map.items():
            bom.register_dependency(ref, depends_on_list)
    match file_format:
        case "cyclonedx-json":
            format_cyclone_json(bom, output)

        case "cyclonedx-xml":
            format_cyclone_xml(bom, output)
