"""The library must stand alone."""

import importlib
import pathlib


def test_handset_bench_imports():
    assert importlib.import_module("handset_bench") is not None


def test_never_imports_its_former_host():
    """This package was extracted from a larger project. It must not reach back."""
    root = pathlib.Path(__file__).parent.parent / "src" / "handset_bench"
    offenders = []
    for path in root.rglob("*.py"):
        for line in path.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith(("import dialtone", "from dialtone")):
                offenders.append(f"{path.name}: {stripped}")
    assert offenders == [], f"must not import dialtone: {offenders}"


def test_core_never_imports_modal():
    """Modal is one way to run the benchmark, never a requirement to use it."""
    root = pathlib.Path(__file__).parent.parent / "src" / "handset_bench"
    offenders = []
    for path in root.rglob("*.py"):
        for line in path.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith(("import modal", "from modal")):
                offenders.append(f"{path.name}: {stripped}")
    assert offenders == [], f"the library must not require modal: {offenders}"
