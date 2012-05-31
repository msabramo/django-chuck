from django_chuck.commands.base import BaseCommand
from django_chuck.commands import create_virtualenv, install_modules, install_virtualenv, create_database, build_snapshot

class Command(BaseCommand):
    help = "Start a new project"

    def __init__(self):
        super(Command, self).__init__()

        self.opts.append(("modules", {
            "help": "modules to install",
            "nargs": "?",
        }))

        self.opts.append(("-a", {
            "help": "Comma seperated list of apps that should get installed by pip",
            "dest": "additional_apps",
            "default": None,
            "nargs": "?",
        }))


    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        create_virtualenv.Command().handle(args, cfg)
        install_modules.Command().handle(args, cfg)
        install_virtualenv.Command().handle(args, cfg)
        build_snapshot.Command().handle(args, cfg)
        create_database.Command().handle(args, cfg)


        self.print_header("SUMMARY")

        installed_modules = self.get_install_modules()

        print "Created project with modules " + ", ".join(installed_modules)

        if self.use_virtualenvwrapper:
            print "\nworkon " + self.site_name
        else:
            print "\nsource " + self.virtualenv_dir + "/bin/activate"

            print "cd " + self.site_dir

        print "django-admin.py createsuperuser"
