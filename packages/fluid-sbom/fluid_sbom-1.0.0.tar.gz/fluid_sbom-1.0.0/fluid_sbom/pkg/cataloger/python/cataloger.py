from fluid_sbom.pkg.cataloger.generic.cataloger import (
    Request,
)
from fluid_sbom.pkg.cataloger.python.parse_pipfile_deps import (
    parse_pipfile_deps,
)
from fluid_sbom.pkg.cataloger.python.parse_poetry_lock import (
    parse_poetry_lock,
)
from fluid_sbom.pkg.cataloger.python.parse_requirements import (
    parse_requirements_txt,
)
from fluid_sbom.pkg.cataloger.python.parse_wheel_egg import (
    parse_weel_or_egg,
)
from fnmatch import (
    fnmatch,
)
import reactivex
from reactivex.abc import (
    ObserverBase,
    SchedulerBase,
)


def on_next_python(
    source: reactivex.Observable[str],
) -> reactivex.Observable[Request]:
    def subscribe(
        observer: ObserverBase[Request],
        scheduler: SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        def on_next(value: str) -> None:
            if fnmatch(value, "*requirements*.txt"):
                observer.on_next(
                    Request(
                        value,
                        parse_requirements_txt,
                        "python-requirements-cataloger",
                    )
                )
            elif any(
                fnmatch(value, x)
                for x in ("*poetry.lock", "poetry.lock", "*/poetry.lock")
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_poetry_lock,
                        "python-poetry-lock-cataloger",
                    )
                )
            elif any(
                fnmatch(value, x)
                for x in (
                    "**/*.egg-info",
                    "**/*dist-info/METADATA",
                    "**/*egg-info/PKG-INFO",
                    "**/*DIST-INFO/METADATA",
                    "**/*EGG-INFO/PKG-INFO",
                )
            ):
                observer.on_next(
                    Request(
                        value,
                        parse_weel_or_egg,
                        "python-installed-package-cataloger",
                    )
                )
            elif fnmatch(value, "**/Pipfile"):
                observer.on_next(
                    Request(
                        value,
                        parse_pipfile_deps,
                        "python-pipfile-package-cataloger",
                    )
                )

        return source.subscribe(
            on_next,
            observer.on_error,
            observer.on_completed,
            scheduler=scheduler,
        )

    return reactivex.create(subscribe)
