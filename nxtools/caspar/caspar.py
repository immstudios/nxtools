__all__ = ["CasparCG"]

import selectors
import socket
import time

theNULL = bytes([0])


if hasattr(selectors, "PollSelector"):
    _TelnetSelector = selectors.PollSelector
else:
    _TelnetSelector = selectors.SelectSelector


class CasparException(Exception):
    """Exception raised for errors in the CasparCG client."""

    pass


class CasparCG:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5250,
        timeout: float = 5,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.rawq = b""
        self.irawq = 0
        self.cookedq = b""
        self.eof = 0

    def open(self):
        """Establish a connection to the host at the given port.

        If the connection is already open, close it first.
        """
        if self.sock:
            self.close()
        self.eof = 0
        self.sock = socket.create_connection((self.host, self.port), self.timeout)

    def close(self) -> None:
        """Close the connection."""
        sock = self.sock
        self.sock = None
        self.eof = True
        if sock:
            sock.close()

    def __del__(self):
        self.close()

    def fileno(self) -> int | None:
        """Return the fileno() of the socket object used internally."""
        # this is needed for select(), do not remove
        if not self.sock:
            return None
        return self.sock.fileno()

    def query(self, command: str, timeout=None) -> str | None:
        """Execute a given AMCP command and return the response"""
        if not self.sock:
            self.open()

        if not self.sock:
            raise CasparException("Connection failed")

        buffer = f"{command}\r\n".encode("utf-8")
        try:
            self.sock.sendall(buffer)
        except ConnectionResetError:
            self.close()
            raise CasparException("AMCP send failed")

        response = self.read(timeout).decode("utf-8")

        if not response:
            raise CasparException("No data")

        if response[:3] == "202":
            return None

        if response[:1] in ["3", "4", "5"]:
            raise CasparException(response)

        if response[:3] in ["201", "200"]:
            data = self.read().decode("utf-8").strip()
            return data

    def read(self, timeout: float | None = None) -> bytes:
        match = b"\r\n"

        n = len(match)
        self.process_rawq()
        i = self.cookedq.find(match)
        if i >= 0:
            i = i + n
            buf = self.cookedq[:i]
            self.cookedq = self.cookedq[i:]
            return buf
        if timeout is not None:
            deadline = time.monotonic() + timeout
        with _TelnetSelector() as selector:
            selector.register(self, selectors.EVENT_READ)
            while not self.eof:
                if selector.select(timeout):
                    i = max(0, len(self.cookedq) - n)
                    self.fill_rawq()
                    self.process_rawq()
                    i = self.cookedq.find(match, i)
                    if i >= 0:
                        i = i + n
                        buf = self.cookedq[:i]
                        self.cookedq = self.cookedq[i:]
                        return buf
                if timeout is not None:
                    timeout = deadline - time.monotonic()
                    if timeout < 0:
                        break

        buf = self.cookedq
        self.cookedq = b""
        if not buf and self.eof and not self.rawq:
            raise EOFError("telnet connection closed")
        return buf

    def process_rawq(self):
        if not self.sock:
            return
        buf = b""
        try:
            while self.rawq:
                c = self.rawq_getchar()
                if c == theNULL:
                    continue
                if c == b"\021":
                    continue
                buf += c
        except EOFError:  # raised by self.rawq_getchar()
            pass
        self.cookedq = self.cookedq + buf

    def rawq_getchar(self):
        """Get next char from raw queue.

        Block if no data is immediately available.  Raise EOFError
        when connection is closed.

        """
        if not self.rawq:
            self.fill_rawq()
            if self.eof:
                raise EOFError
        c = self.rawq[self.irawq : self.irawq + 1]
        self.irawq = self.irawq + 1
        if self.irawq >= len(self.rawq):
            self.rawq = b""
            self.irawq = 0
        return c

    def fill_rawq(self) -> None:
        """Fill raw queue from exactly one recv() system call.

        Block if no data is immediately available.  Set self.eof when
        connection is closed.

        """

        assert self.sock is not None

        if self.irawq >= len(self.rawq):
            self.rawq = b""
            self.irawq = 0
        # The buffer size should be fairly small so as to avoid quadratic
        # behavior in process_rawq() above
        buf = self.sock.recv(50)
        self.eof = not buf
        self.rawq = self.rawq + buf

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        # Keep linters happy
        _ = type, value, traceback
        self.close()

