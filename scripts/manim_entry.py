"""Run the Manim CLI and always terminate.

Manim 0.19 can hang after an exception in ``construct`` (its file-writer
thread keeps the interpreter alive). This wrapper exits hard with a non-zero
code so CI fails fast instead of timing out.
"""

import os
import sys
import traceback

from manim.__main__ import main

code = 0
try:
    main(standalone_mode=False)
except SystemExit as exc:
    code = exc.code if isinstance(exc.code, int) else 1
except BaseException:  # noqa: BLE001
    traceback.print_exc()
    code = 1
sys.stdout.flush()
sys.stderr.flush()
os._exit(code)
