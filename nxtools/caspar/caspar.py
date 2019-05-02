import telnetlib

from nxtools import logging, log_traceback, PYTHON_VERSION, decode_if_py3, encode_if_py3

__all__ = [
        "CasparCG",
        "CasparResponse"
    ]

class CasparResponse(object):
    """Caspar query response object"""
    def __init__(self, code, data):
        self.code = code
        self.data = data

    @property
    def response(self):
        return self.code

    @property
    def is_error(self):
        """Returns True if query failed"""
        return self.code >= 300

    @property
    def is_success(self):
        """Returns True if query succeeded"""
        return self.code < 300

    def __repr__(self):
        if self.is_success:
            return "Caspar response: OK"
        return "Caspar response: Error - {}".format(self.data)

    def __len__(self):
        return self.is_success


class CasparCG(object):
    """CasparCG client object"""
    def __init__(self, host, port=5250, timeout=5):
        assert isinstance(port, int) and port <= 65535, "Invalid port number"
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connection = False

    def connect(self):
        """Create connection to CasparCG Server"""
        try:
            self.connection = telnetlib.Telnet(self.host, self.port, timeout=self.timeout)
        except Exception:
            log_traceback()
            return False
        return True

    def query(self, query, **kwargs):
        """Send AMCP command"""
        if not self.connection:
            if not self.connect():
                return CasparResponse(500, "Unable to connect CasparCG server")

        query = query.strip()
        if kwargs.get("verbose", True):
            if not query.startswith("INFO"):
                logging.debug("Executing AMCP: {}".format(query))
        query += "\r\n"

        if PYTHON_VERSION >= 3:
            query = bytes(query.encode("utf-8"))
            delim = bytes("\r\n".encode("utf-8"))
        else:
            delim = "\r\n"

        try:
            self.connection.write(query)
            result = self.connection.read_until(delim).strip()
        except Exception:
            log_traceback()
            return CasparResponse(500, "Query failed")

        if PYTHON_VERSION >= 3:
            result = result.decode("UTF-8")

        if not result:
            return CasparResponse(500, "No result")

        try:
            if result[0:3] == "202":
                return CasparResponse(202, "No result")

            elif result[0:3] in ["201", "200"]:
                stat = int(result[0:3])
                result = decode_if_py3(self.connection.read_until(delim)).strip()
                return CasparResponse(stat, result)

            elif int(result[0:1]) > 3:
                stat = int(result[0:3])
                return CasparResponse(stat, result)
        except Exception:
            log_traceback()
            return CasparResponse(500, "Malformed result: {}".format(result))
        return CasparResponse(500, "Unexpected result: {}".format(result))
