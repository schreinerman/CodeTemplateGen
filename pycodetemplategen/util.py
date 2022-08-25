import sys
import struct

def hexify(s, uppercase=True):
    format_str = "%02X" if uppercase else "%02x"
    return "".join(format_str % c for c in s)

class FatalError(RuntimeError):
    """
    Wrapper class for runtime errors that aren't caused by internal bugs, but by
    CodeTemplateGen
    """

    def __init__(self, message):
        RuntimeError.__init__(self, message)

    @staticmethod
    def WithResult(message, result):
        """
        Return a fatal error object that appends the hex values of
        'result' and its meaning as a string formatted argument.
        """

        err_defs = {
            0x101: "Out of memory",
            0x102: "Invalid argument",
        }

        err_code = struct.unpack(">H", result[:2])
        message += " (result was {}: {})".format(
            hexify(result), err_defs.get(err_code[0], "Unknown result")
        )
        return FatalError(message)