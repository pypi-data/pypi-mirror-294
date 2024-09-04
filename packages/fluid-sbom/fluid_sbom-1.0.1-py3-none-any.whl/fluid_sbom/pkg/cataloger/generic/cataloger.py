from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.pkg.cataloger.alpine.parse_apk_db import (
    parse_apk_db,
)
from fluid_sbom.pkg.cataloger.arch.parse_alpm import (
    parse_alpm_db,
)
from fluid_sbom.pkg.cataloger.debian.parse_dpkg_db import (
    parse_dpkg_db,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
    Parser,
)
from fluid_sbom.pkg.cataloger.redhat.parse_rpm_db import (
    parse_rpm_db,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fnmatch import (
    fnmatch,
)
import logging
import reactivex
from reactivex import (
    Observable,
    operators as ops,
)
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)
from reactivex.scheduler import (
    ThreadPoolScheduler,
)
from typing import (
    Callable,
    NamedTuple,
)

LOGGER = logging.getLogger(__name__)


class Request(NamedTuple):
    real_path: str
    parser: Parser
    parser_name: str


class Task(NamedTuple):
    location: Location
    parser: Parser
    parser_name: str


pool_scheduler = ThreadPoolScheduler(10)


def _apply_scheduler(obs: Observable) -> Observable:  # NOSONAR
    return obs.pipe(ops.subscribe_on(pool_scheduler))


def execute_parsers(
    resolver: Resolver, environment: Environment
) -> Callable[[Observable[Task]], Observable]:
    def _handle(source: Observable[Task]) -> Observable:
        def subscribe(
            observer: ObserverBase[tuple[list[Package], list[Relationship]]],
            scheduler: SchedulerBase | None = None,
        ) -> reactivex.abc.DisposableBase:
            def on_next(value: Task) -> None:
                LOGGER.info("Working on %s", value.location.access_path)
                content_reader = resolver.file_contents_by_location(
                    value.location
                )
                if content_reader is not None and (
                    result := value.parser(
                        resolver,
                        environment,
                        LocationReadCloser(value.location, content_reader),
                    )
                ):
                    discover_packages, relationships = result
                    for pkg in discover_packages:
                        pkg.found_by = value.parser_name
                    observer.on_next((discover_packages, relationships))

            return source.subscribe(
                on_next,
                observer.on_error,
                observer.on_completed,
                scheduler=scheduler,
            )

        return reactivex.create(subscribe)

    return _handle


def on_next_db_file(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            if "lib/apk/db/installed" in value:
                observer.on_next(
                    Request(
                        value,
                        parse_apk_db,
                        "apk-db-selector",
                    )
                )
            elif any(
                fnmatch(value, x)
                for x in (
                    "**/var/lib/dpkg/status",
                    "*var/lib/dpkg/status",
                    "/var/lib/dpkg/status",
                    "**/var/lib/dpkg/status.d/*",
                    "*var/lib/dpkg/status.d/*",
                    "/var/lib/dpkg/status.d/*",
                    "**/lib/opkg/info/*.control",
                    "*lib/opkg/info/*.control",
                    "/lib/opkg/info/*.control",
                    "**/lib/opkg/status",
                    "*lib/opkg/status",
                    "/lib/opkg/status",
                )
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_dpkg_db,
                        "dpkg-db-selector",
                    )
                )
            elif any(
                fnmatch(value, pattern)
                for pattern in (
                    "**/var/lib/pacman/local/**/desc",
                    "var/lib/pacman/local/**/desc",
                    "/var/lib/pacman/local/**/desc",
                )
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_alpm_db,
                        "alpm-db-selector",
                    )
                )
            elif any(
                fnmatch(value, x)
                for x in (
                    (
                        "**/{var/lib,usr/share,usr/lib/sysimage}"
                        "/rpm/{Packages,Packages.db,rpmdb.sqlite}"
                    ),
                    (
                        "/{var/lib,usr/share,usr/lib/sysimage}"
                        "/rpm/{Packages,Packages.db,rpmdb.sqlite}"
                    ),
                    "**/rpmdb.sqlite",
                )
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_rpm_db,
                        "environment-parser",
                    )
                )

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
