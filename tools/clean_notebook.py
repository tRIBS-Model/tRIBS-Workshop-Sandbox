#!/usr/bin/env python3
"""Normalize a notebook for committing. Used as a git clean filter.

Reads a .ipynb on stdin, writes the normalized notebook to stdout:

  - kernelspec is pinned to the generic "python3" so the codespace's Jupyter
    extension auto-selects the image's interpreter instead of showing a picker
    (see .devcontainer/devcontainer.json). Running a notebook against a local
    venv otherwise stamps that venv's kernel name into the file.
  - language_info.version is dropped. It is stamped by whichever kernel ran
    the notebook, is not used for kernel selection, and drifts with the base
    image's Python patch release, so committing it is pure diff noise.
  - cell outputs and execution counts are cleared.

The working tree copy is never touched; only what git stores is normalized.
Anything that isn't a parseable notebook is passed through unchanged.
"""

import json
import sys

KERNELSPEC = {"display_name": "Python 3", "language": "python", "name": "python3"}


def main() -> int:
    raw = sys.stdin.read()
    try:
        nb = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        sys.stdout.write(raw)
        return 0

    if not isinstance(nb, dict) or "cells" not in nb:
        sys.stdout.write(raw)
        return 0

    metadata = nb.setdefault("metadata", {})
    metadata["kernelspec"] = dict(KERNELSPEC)
    metadata.get("language_info", {}).pop("version", None)

    for cell in nb["cells"]:
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    json.dump(nb, sys.stdout, indent=1, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
