import re
import os
from django_chuck.commands.base import BaseCommand
from django_chuck.commands import sync_database, migrate_database


class Command(BaseCommand):
    help = "Sync, migrate database and load fixtures"

    def __init__(self):
        super(Command, self).__init__()

        self.opts.append(("fixture_files", {
            "help": "Comma separated list of fixture files to load",
            "nargs": "?",
        }))

        self.opts.append(("extra_syncdb_options", {
            "help": "Options to append at syncdb command",
            "nargs": "?",
        }))

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        sync_database.Command().handle(args, cfg)
        migrate_database.Command().handle(args, cfg)

        try:
            if args.fixture_files:
                for fixture_file in re.split("\s*,\s*", args.fixture_files):
                    self.db_cleanup()
                    self.load_fixtures(os.path.join(self.site_dir, "fixtures", fixture_file))
        except AttributeError:
            pass

