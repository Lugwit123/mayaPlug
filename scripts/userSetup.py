"""
Deadline Bootstrapper script which loads the Maya integrated submitter when Maya starts up.
"""

from __future__ import absolute_import
from distutils.spawn import find_executable
import json
import os
import subprocess

import maya.cmds as cmds
import maya.mel as mel

try:
    from typing import List
except ImportError:
    pass

# Maya always uses / for it's path separators regardless of platform
PATH_SEP = '/'


def get_deadlinecommand():
    # type: () -> str
    """
    Finds the Deadline Command executable as it is installed on your machine by searching in the following order:
    * The DEADLINE_PATH environment variable
    * The PATH environment variable
    * The file /Users/Shared/Thinkbox/DEADLINE_PATH
    """

    for env in ("DEADLINE_PATH", "PATH"):
        try:
            env_value = os.environ[env]
        except KeyError:
            # if the error is a key error it means that DEADLINE_PATH is not set.
            # however Deadline command may be in the PATH or on OSX it could be in the file /Users/Shared/Thinkbox/DEADLINE_PATH
            continue

        exe = find_executable("deadlinecommand", env_value)
        if exe:
            return exe

    # On OSX, we look for the DEADLINE_PATH file if the environment variable does not exist.
    if os.path.exists("/Users/Shared/Thinkbox/DEADLINE_PATH"):
        with open("/Users/Shared/Thinkbox/DEADLINE_PATH") as dl_file:
            deadline_bin = dl_file.read().strip()
        exe = find_executable("deadlinecommand", deadline_bin)
        if exe:
            return exe

    raise Exception("Deadline could not be found.  Please ensure that Deadline is installed.")


def call_deadlinecommand(arguments, format_output_as_json=False):
    # type: (List[str], bool) -> str
    """
    Calls DeadlineCommand with a given list of arguments.
    If json_output is true the output is returned as a json dictionary.
    Otherwise the raw string is output is returned.
    """
    command = [get_deadlinecommand()]
    if format_output_as_json:
        # JSON formatting option must come directly after the Deadline Command executable in the argument list.
        command.append('-prettyJSON')
    command.extend(arguments)

    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = proc.communicate()

    # py2/3 compatible manner to ensure we have a str
    if not isinstance(output, str):
        output = output.decode()  # type: ignore

    if format_output_as_json:
        json_out = json.loads(output)
        if json_out["ok"]:
            return json_out["result"]
        else:
            raise Exception(json_out["result"])
    else:
        if proc.returncode:
            raise Exception(output)
        return output  # type: ignore


def GetMayaSubmissionDir():
    # type: () -> str
    """
    Uses Deadline command to pull the main Maya integrated submitter.
    """
    json_out = call_deadlinecommand(["-GetRepositoryPath", "submission/Maya/Main"], format_output_as_json=True)
    return json_out.replace(os.sep, PATH_SEP)


def load_deadline_submitters():
    # type: () -> None
    """
    Pulls the Deadline integrated submitter from the Deadline repository and sources the mel file.
    """
    # Get the repository path
    try:
        submission_dir = GetMayaSubmissionDir()
    except Exception as e:
        cmds.warning("Failed to pull Deadline Integrated submitter: %s" % e)
        return

    submission_file = '{}/SubmitMayaToDeadline.mel'.format(submission_dir)

    if os.path.isfile(submission_file):
        mel.eval('source "{}";'.format(submission_file))
    else:
        cmds.warning('Deadline submission directory does not contain SubmitMayaToDeadlne.mel')


# Have maya load the submitters after it finishes loading all mel script files.
cmds.evalDeferred(load_deadline_submitters)
# C:/ProgramData/Thinkbox/Deadline10/submitters/Maya