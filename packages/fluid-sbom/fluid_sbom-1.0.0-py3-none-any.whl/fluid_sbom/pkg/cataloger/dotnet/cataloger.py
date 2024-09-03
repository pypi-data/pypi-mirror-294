from fluid_sbom.pkg.cataloger.dotnet.parse_csproj import (
    parse_csproj,
)
from fluid_sbom.pkg.cataloger.dotnet.parse_dotnet_package_config import (
    parse_dotnet_pkgs_config,
)
from fluid_sbom.pkg.cataloger.dotnet.parse_dotnet_package_lock import (
    parse_dotnet_package_lock,
)
from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
)
from fnmatch import (
    fnmatch,
)
import reactivex
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)


def on_next_dotnet(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            if any(
                fnmatch(value, x)
                for x in (
                    "**/packages.config",
                    "packages.config",
                )
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_dotnet_pkgs_config,
                        "dotnet-parse-packages-config",
                    )
                )
            elif any(
                fnmatch(value, x)
                for x in (
                    "**/packages.lock.json",
                    "packages.lock.json",
                )
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_dotnet_package_lock,
                        "dotnet-parse-package-lock",
                    )
                )
            elif any(
                fnmatch(value, x)
                for x in (
                    "**/project.csproj",
                    "project.csproj",
                )
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_csproj,
                        "dotnet-parse-csproj",
                    )
                )

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
