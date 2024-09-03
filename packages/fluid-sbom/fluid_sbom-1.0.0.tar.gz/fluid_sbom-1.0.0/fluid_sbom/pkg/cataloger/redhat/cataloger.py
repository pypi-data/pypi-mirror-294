from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
)
from fluid_sbom.pkg.cataloger.redhat.parse_rpm_db import (
    parse_rpm_db,
)
from fnmatch import (
    fnmatch,
)
import reactivex
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)


def on_next_redhat(
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
                    # /var/lib/rpm/Packages
                    # /var/lib/rpm/Packages.db
                    "/var/lib/rpm/rpmdb.sqlite",
                    # /usr/share/rpm/Packages
                    # /usr/share/rpm/Packages.db
                    "/usr/share/rpm/rpmdb.sqlite",
                    # /usr/lib/sysimage/rpm/Packages
                    # /usr/lib/sysimage/rpm/Packages.db
                    "/usr/lib/sysimage/rpm/rpmdb.sqlite",
                )
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_rpm_db,
                        "redhat-parse-rpmdb",
                    )
                )
            if any(fnmatch(value, x) for x in ("**/*.rpm", "*.rpm")):
                observer.on_next(
                    Request(
                        value,
                        parse_rpm_db,
                        "redhat-parse-rpmdb",
                    )
                )

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
