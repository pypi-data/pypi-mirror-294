from _typeshed import Incomplete

from .exceptions import EOF as EOF
from .exceptions import TIMEOUT as TIMEOUT
from .exceptions import ExceptionPexpect as ExceptionPexpect
from .spawnbase import SpawnBase as SpawnBase
from .utils import poll_ignore_interrupts as poll_ignore_interrupts
from .utils import select_ignore_interrupts as select_ignore_interrupts
from .utils import split_command_line as split_command_line
from .utils import which as which

from os import _Environ

PY3: Incomplete


class spawn(SpawnBase):
    use_native_pty_fork: Incomplete
    STDIN_FILENO: Incomplete
    STDOUT_FILENO: Incomplete
    STDERR_FILENO: Incomplete
    str_last_chars: int
    cwd: Incomplete
    env: Incomplete
    echo: Incomplete
    ignore_sighup: Incomplete
    command: Incomplete
    args: Incomplete
    name: str
    use_poll: Incomplete

    def __init__(
        self,
        command,
        args=...,
        timeout: int = ...,
        maxread: int = ...,
        searchwindowsize: Incomplete | None = ...,
        logfile: Incomplete | None = ...,
        cwd: Incomplete | None = ...,
        env: _Environ[str] | None = ...,
        ignore_sighup: bool = ...,
        echo: bool = ...,
        preexec_fn: Incomplete | None = ...,
        encoding: Incomplete | None = ...,
        codec_errors: str = ...,
        dimensions: Incomplete | None = ...,
        use_poll: bool = ...,
    ) -> None:
        ...

    child_fd: int
    closed: bool

    def close(self, force: bool = ...) -> None:
        ...

    def isatty(self):
        ...

    def waitnoecho(self, timeout: int = ...):
        ...

    def getecho(self):
        ...

    def setecho(self, state):
        ...

    def read_nonblocking(self, size: int = ..., timeout: Incomplete = ...):
        ...

    def write(self, s) -> None:
        ...

    def writelines(self, sequence) -> None:
        ...

    def send(self, s):
        ...

    def sendline(self, s: str = ...):
        ...

    def sendcontrol(self, char):
        ...

    def sendeof(self) -> None:
        ...

    def sendintr(self) -> None:
        ...

    @property
    def flag_eof(self):
        ...

    @flag_eof.setter
    def flag_eof(self, value) -> None:
        ...

    def eof(self):
        ...

    def terminate(self, force: bool = ...):
        ...

    status: Incomplete
    exitstatus: Incomplete
    signalstatus: Incomplete
    terminated: bool

    def wait(self):
        ...

    def isalive(self):
        ...

    def kill(self, sig) -> None:
        ...

    def getwinsize(self):
        ...

    def setwinsize(self, rows, cols):
        ...

    def interact(
        self,
        escape_character=...,
        input_filter: Incomplete | None = ...,
        output_filter: Incomplete | None = ...,
    ) -> None:
        ...


def spawnu(*args, **kwargs):
    ...
