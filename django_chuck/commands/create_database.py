from django_chuck.commands.base import BaseCommand
from django_chuck.commands import sync_database, migrate_database


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

        sync_database.Command().handle(args, cfg)

        if "south" in self.get_install_modules():
            migrate_database.Command().handle(args, cfg)
