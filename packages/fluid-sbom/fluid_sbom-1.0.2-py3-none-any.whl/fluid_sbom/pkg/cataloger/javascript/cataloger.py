from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
)
from fluid_sbom.pkg.cataloger.javascript.parse_package_json import (
    parse_package_json,
)
from fluid_sbom.pkg.cataloger.javascript.parse_package_lock import (
    parse_package_lock,
)
from fluid_sbom.pkg.cataloger.javascript.parse_pnpm_lock import (
    parse_pnpm_lock,
)
from fluid_sbom.pkg.cataloger.javascript.parse_yarn_lock import (
    parse_yarn_lock,
)
from fnmatch import (
    fnmatch,
)
import reactivex
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)


def on_next_javascript(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            if any(
                fnmatch(value, x) for x in ("**/package.json", "package.json")
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_package_json,
                        "javascript-parse-package-json",
                    )
                )
            elif any(
                fnmatch(value, x)
                for x in ("**/package-lock.json", "package-lock.json")
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_package_lock,
                        "javascript-parse-package-lock",
                    )
                )

            elif any(fnmatch(value, x) for x in ("**/yarn.lock", "yarn.lock")):
                observer.on_next(
                    Request(
                        value,
                        parse_yarn_lock,
                        "javascript-parse-yarn-lock",
                    )
                )
            elif any(
                fnmatch(value, x)
                for x in ("**/pnpm-lock.yaml", "pnpm-lock.yaml")
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_pnpm_lock,
                        "javascript-parse-pnpm-lock",
                    )
                )

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
