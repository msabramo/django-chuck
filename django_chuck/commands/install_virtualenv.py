from django_chuck.commands.base import BaseCommand
import re
import os


class Command(BaseCommand):
    help = "Install all requirements in virtualenv"

    def __init__(self):
        super(Command, self).__init__()

        self.opts.append(("-a", {
            "help": "Comma seperated list of apps that should get installed by pip",
            "dest": "additional_apps",
            "default": None,
            "nargs": "?",
        }))



    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        self.print_header("INSTALL VIRTUALENV")
        self.execute_in_project("pip install -r " + os.path.join(self.site_dir, "requirements", "requirements_dev.txt"))

        # Install additional apps
        if self.additional_apps:
            for app in re.split("\s*,\s*", self.additional_apps):
                self.execute_in_project("pip install " + app)