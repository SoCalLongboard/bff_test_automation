# Standard library imports
from os import environ

# 3rd party library imports
import pytest

REQUIRED_ENVARS = [
    "BFF_ROOT",
    "ENVIRONMENT_CONTEXT",
]
FOUND_ENVARS = environ.keys()


def pytest_configure(config):
    bff_root = environ["BFF_ROOT"]
    config._metadata["Sprout (BFF) root"] = bff_root

    if "preview" in bff_root:
        config._metadata["Test environment"] = "preview"
    else:
        config._metadata["Test environment"] = environ["ENVIRONMENT_CONTEXT"]


def pytest_html_report_title(report):
    report.title = "BFF (Sprout Server API) Test Automation"


def pytest_runtest_call():
    _log_required_envars()


def pytest_sessionstart():
    _check_required_envars()
    _check_required_keypair()


def _check_required_envars():
    max_length = max(len(item) for item in REQUIRED_ENVARS)

    print()
    for envar in sorted(REQUIRED_ENVARS):
        if envar not in FOUND_ENVARS:
            pytest.exit(f"Required environment variable '{envar}' undefined -- quitting...")
        else:
            print(f"{envar:<{max_length}} : {environ[envar]}")
    print()


def _check_required_keypair():
    if "BFF_PLENTY_API_KEY" in FOUND_ENVARS:
        if "BFF_PLENTY_API_SECRET" not in FOUND_ENVARS:
            pytest.exit("BFF_PLENTY_API_KEY defined but BFF_PLENTY_API_SECRET missing -- quitting... ")
        else:
            print("Using BFF_PLENTY_API_KEY/BFF_PLENTY_API_SECRET keypair...")
            print()
            return

    if "PLENTY_API_KEY" in FOUND_ENVARS:
        if "PLENTY_API_SECRET" not in FOUND_ENVARS:
            pytest.exit("PLENTY_API_KEY defined but PLENTY_API_SECRET missing -- quitting... ")
        else:
            print("Using PLENTY_API_KEY/PLENTY_API_SECRET keypair...")
            print()
            return

    pytest.exit("PLENTY_API keypair not defined -- quitting...")


def _log_required_envars():
    max_length = max(len(item) for item in REQUIRED_ENVARS)

    print()
    for envar in sorted(REQUIRED_ENVARS):
        if envar not in FOUND_ENVARS:
            print(f"*** Required environment variable '{envar}' undefined ***")
        else:
            print(f"{envar:<{max_length}} : {environ[envar]}")
    print()
