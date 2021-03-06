import io
import os
import re
import sys
import atexit
from textwrap import dedent
FS = re.compile(r"\s+", re.UNICODE)
pattern_action = re.compile(r"(.*?)\{([^\}]+?)\}", re.UNICODE)

def _parse_actions(script):
    """Parse the script to produce a dict of patterns and actions.

    :param script: The pawn script to parse, must be a str not a filename
    :type script: str
    :rtype: dict
    :returns: A mapping of pattern to action
    """
    script = dedent(script)
    ret = {}
    for pattern, action in pattern_action.findall(script):
        if not pattern:
            pattern = ".*"
        ret[pattern] = dedent(action)
    return ret


def pawn(script, files):
    """A simple interpreter for a language based on Python and AWK.

    The rules are simple, and in a great act of blasphemy, they rely heavily
    on curly-braces "{}".

    So, a pawn program consists of patterns and actions. Patterns are regular
    expressions which are evaluated and actions which consist of Python source
    code.

    The main concept with pawn is that it is executed with two contexts the first
    is of a plain text input file and the second is a pawn script. Each line of
    the input is examined within the context of the pawn script. Based on the
    defined patterns a set of actions is built and executed in order.

    The Python source code which comprises an action is evaluated with the following
    global variables defined:

    * LINE: The current line being examined
    * FIELDS: A list containing the fields into which the LINE was split
    * FS: The field seperator, defaults to any whitespace

    :param script: The script to execute, can be passed as-is or a filename can be passed which will be read for the script
    :param files: Can be a single file-like object or a str containing a filename or a list of either
    :type script: str
    :type files: str file list
    :rtype: None
    :returns: None
    """
    if not isinstance(files, list):
        files = [files]
    for index, file in enumerate(list(files)):
        if isinstance(file, str):
            files[index] = io.open(file, "r")
            atexit.register(files[index].close)
    if os.path.exists(script) and os.path.isfile(script):
        with io.open(script, "r") as fp:
            patterns = _parse_actions(fp.read())
    else:
        patterns = _parse_actions(script)
    environ = {
        "FS": FS.pattern
    }
    if "BEGIN" in patterns:
        begin = patterns.pop("BEGIN")
        exec(begin, environ)
    end = None
    if "END" in patterns:
        end = patterns.pop("END")
    for file in files:
        for line in file:
            environ["LINE"] = line.rstrip()
            environ["FIELDS"] = list(filter(lambda x: x, FS.split(line)))
            for pattern in patterns:
                if re.search(pattern, line):
                    exec(patterns[pattern], environ)
    if end:
        exec(end, environ)
