import bugsnag
from bugsnag_client import (
    add_batch_metadata as bugsnag_add_batch_metadata,
    remove_nix_hash as bugsnag_remove_nix_hash,
)
import logging
import os


def initialize_bugsnag() -> None:
    bugsnag.before_notify(bugsnag_add_batch_metadata)
    bugsnag.before_notify(bugsnag_remove_nix_hash)
    bugsnag.configure(
        ignore_classes=[
            "SystemExit",
        ],
        breadcrumb_log_level=logging.DEBUG,
        notify_release_stages=["production"],
        project_root=os.path.dirname(os.path.abspath(__file__)),
    )
    bugsnag.start_session()
