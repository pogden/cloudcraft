from fabric.api import local, run, cd, put
from fabric.colors import green, red

import logging
import os
import StringIO
import traceback

REMOTE_PATH = "~/.cloudcraft/"
BOOTSTRAP_PATH = "bootstrap/"
SCRIPTS_PATH = "scripts/"

log = logging.getLogger("cloudcraft")


def run_remote(command, command_args=[], remote_vars={}):
    try:
        run("mkdir -p %s" % REMOTE_PATH)
        script_file = "{0}/{1}.sh".format(SCRIPTS_PATH, command)
        remote_path = "{0}/{1}.sh".format(REMOTE_PATH, command)
        prepared_buffer = StringIO.StringIO()
        for k, v in remote_vars.items():
            prepared_buffer.write('%s="%s"\n' %(k,v))
        with open(script_file, "r") as fh:
            prepared_buffer.write(fh.read())
        if command == "bootstrap":
            print(green("----- Syncing lib.sh -----"))
            put(SCRIPTS_PATH + "lib.sh", REMOTE_PATH + "lib.sh")
        put(prepared_buffer, remote_path)
        with cd(REMOTE_PATH):
            return run("bash ./{0}.sh {1}".format(command, " ".join(command_args)), pty=False, combine_stderr=False)
    except ValueError, IOError:
        print(traceback.format_exc())
        log.error(red("Couldn't connect to the instance"))
        return
    except:
        log.error(red("Error when executing command {0}".format(command)))
        return
