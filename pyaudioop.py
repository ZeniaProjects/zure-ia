"""Compatibility shim for pydub on Python 3.13+/3.14.

pydub imports `pyaudioop` when the stdlib `audioop` is unavailable.
On newer Python runtimes, the backport package `audioop-lts` exposes the
module as `audioop`, while pydub still looks for `pyaudioop`.
This file makes that import succeed without changing the application logic.
"""

from audioop import *  # noqa: F401,F403

import audioop as _audioop

# Re-export the module under the expected name for compatibility with third-party libs
__all__ = [name for name in globals() if not name.startswith("_")]
