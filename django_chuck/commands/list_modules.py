import os
from django_chuck.commands.base import BaseCommand

class Command(BaseCommand):
    help = "Shows all available modules"

    def __init__(self):
        super(Command, self).__init__()

        # Disable default checks because this command isn't project-related
        self.no_default_checks = True

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        self.print_header("AVAILABLE MODULES")

        for module_basedir in self.module_basedirs:
            for module_name in os.listdir(module_basedir):
                print module_name

