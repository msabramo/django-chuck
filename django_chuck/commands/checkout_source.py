import os
import sys
import shutil
import tempfile
import subprocess
from django_chuck.commands.base import BaseCommand


class Command(BaseCommand):
    help = "Checkout the source code"

    def __init__(self):
        super(Command, self).__init__()

        self.no_default_checks = True

        self.opts.append((
            "checkout_url", {
                "help": "repository url",
            }))

        self.opts.append((
            "-cd", {
                "help": "destination directory",
                "dest": "checkout_destdir",
                "default": "",
                "nargs": "?"
            }),
        )

        self.opts.append((
            "-b", {
                "help": "branch to checkout / clone",
                "dest": "branch",
                "default": "",
                "nargs": "?"
            }),
        )


    def signal_handler(self):
        if os.path.exists(self.checkout_destdir):
            print "Deleting checkout directory " + self.checkout_destdir
            shutil.rmtree(self.checkout_destdir)


    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        if not self.checkout_url:
            raise ValueError("checkout_url is not defined")

        if not self.checkout_destdir:
            self.checkout_destdir = tempfile.mkdtemp()

        self.print_header("CHECKOUT SOURCE")

        if os.path.exists(self.checkout_destdir):
            answer = raw_input("Checkout dir exists. Use old source? <Y/n>: ")

            if answer.lower() == "n":
                shutil.rmtree(self.checkout_destdir)
            else:
                return

        if self.version_control_system.lower() == "cvs":
            if self.branch:
                cmd ="cvs checkout -r " + self.branch + " " + self.checkout_url + " " + self.checkout_destdir
            else:
                cmd ="cvs checkout " + self.checkout_url + " " + self.checkout_destdir
        elif self.version_control_system.lower() == "svn":
            cmd = "svn checkout " + self.checkout_url + " " + self.checkout_destdir
        elif self.version_control_system.lower() == "hg":
            if self.branch:
                cmd = "hg clone " + self.checkout_url + " -r " + self.branch + " " + self.checkout_destdir
            else:
                cmd = "hg clone " + self.checkout_url + " " + self.checkout_destdir
        else:
            if self.branch:
                cmd = "git clone " + self.checkout_url + " -b " + self.branch + " " + self.checkout_destdir
            else:
                cmd = "git clone " + self.checkout_url + " " + self.checkout_destdir

        cmd_successful = os.system(cmd)

        if cmd_successful > 0:
            self.kill_system()
