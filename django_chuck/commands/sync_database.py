import os
from django_chuck.commands.base import BaseCommand

class Command(BaseCommand):
    help = "Sync and migrate database"

    def __init__(self):
        super(Command, self).__init__()

        self.opts.append(("extra_syncdb_options", {
            "help": "Options to append at syncdb command",
            "nargs": "?",
        }))

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        if not self.django_settings:
            raise ValueError("django_settings is not defined")

        self.print_header("SYNC DATABASE")
        os.chdir(self.site_dir)
        self.execute_in_project("django-admin.py syncdb --noinput")
