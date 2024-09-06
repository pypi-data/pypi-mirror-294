""" Print function. Severity:

debug = prints all other severities
warning = prints warning + info
info = prints only info

"""

import sys
import os


def info(string):
    """Gets printed when Linux environment variable
    EVC_MANAGER_VERBOSITY is set to 'info'"""
    if os.environ["EVC_MANAGER_QUIET_MODE"] == "False":
        print(string)


def warn(string):
    """Gets printed when Linux environment variable
    EVC_MANAGER_VERBOSITY is set to 'debug' or 'warning'"""

    if os.environ["EVC_MANAGER_VERBOSITY"] in ["warning", "debug"]:
        print(f"Warn: {string}")


def debug(string):
    """Gets printed when Linux environment variable
    EVC_MANAGER_VERBOSITY is set to 'debug'"""

    if os.environ["EVC_MANAGER_VERBOSITY"] in ["debug"]:
        sys.stderr.write(f"Debug: {string}")


def process_result(msg=None):
    """Process results provided by all methods"""
    attention_required = False
    for result in msg:
        if result["result"] == "error":
            attention_required = True

    return {"results": {"msgs": msg}, "attention_required": attention_required}
