from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
)
from fluid_sbom.pkg.cataloger.swift.parse_package_resolved import (
    parse_package_resolved,
)
from fluid_sbom.pkg.cataloger.swift.parse_podfile_lock import (
    parse_podfile_lock,
)
from fnmatch import (
    fnmatch,
)
import reactivex
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)


def on_next_swift(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            if any(
                fnmatch(value, x)
                for x in ("**/Package.resolved", "**/.package.resolved")
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_package_resolved,
                        "parse-swift-parse-package-resolved",
                    )
                )
            elif fnmatch(value, "**/Podfile.lock"):
                observer.on_next(
                    Request(
                        value,
                        parse_podfile_lock,
                        "parse-swift-parse-podfile-lock",
                    )
                )

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
