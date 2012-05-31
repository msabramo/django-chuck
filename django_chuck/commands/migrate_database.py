from django_chuck.commands.base import BaseCommand
import os

class Command(BaseCommand):
    help = "Migrate database"

    def __init__(self):
        super(Command, self).__init__()

        self.opts.append(("extra_migrate_options", {
            "help": "Options to append at migrate command",
            "nargs": "?",
        }))

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        if not self.django_settings:
            raise ValueError("django_settings is not defined")

        if not self.virtualenv_dir:
            raise ValueError("virtualenv_dir is not defined")

        self.print_header("MIGRATE DATABASE")
        os.chdir(self.site_dir)
        self.execute_in_project("django-admin.py migrate")
