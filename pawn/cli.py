import pawn
import sys
import argparse

def main(argv=None):
    """Command line interface for pawn.

    :param argv: A list containing arguments with which to invoke pawn. If None (the default) sys.argv will be used.
    :type argv: list
    :returns: None
    :rtype: None
    """
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(
        prog="pawn.py",
        description="A programming language made from combining "
                    "AWK, Python and awesomeness",
        epilog="Copyright 2016 iLoveTux - all rights reserved"
    )
    parser.add_argument("script", nargs="?", default=None,
                        help="The Pawn script to execute")
    parser.add_argument("files", nargs=argparse.REMAINDER,
                        help="The input file(s) which to examine")
    args = parser.parse_args(argv)
    kwargs = {
        "script": args.script,
        "files": args.files,
    }
    pawn.pawn(**kwargs)
