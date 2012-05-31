import os
import sys
import shutil
from django_chuck.commands.base import BaseCommand
from django_chuck.commands import checkout_source, create_virtualenv, install_virtualenv, sync_database, migrate_database
import django_chuck


class Command(BaseCommand):
    help = "Checkout and setup an existing project"

    def __init__(self):
        self.opts = [
            ("checkout_url", {
                "help": "repository url",
            })
        ]

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

        self.no_default_checks = True


    def handle(self,args, cfg):
        super(Command, self).handle(args, cfg)

        checkout_cmd = checkout_source.Command()
        checkout_cmd.handle(args, cfg)
        cfg["checkout_destdir"] = checkout_cmd.checkout_destdir

        if not os.path.exists(self.checkout_destdir):
            print "Checkout failed! :("
            sys.exit(0)

        chuck_setup_file = os.path.join(cfg["checkout_destdir"], "chuck_setup.py")
        chuck_setup_required_params = [
            "project_prefix",
            "project_name",
            "django_settings",
        ]

        # Import chuck_setup file
        if os.access(chuck_setup_file, os.R_OK):
            chuck_setup_path = os.path.dirname(chuck_setup_file)
            sys.path.insert(0, chuck_setup_path)
            import chuck_setup

            for param in chuck_setup_required_params:
                if not getattr(chuck_setup, param):
                    print "Parameter " + param + " is missing in chuck_setup.py!"
                    sys.exit(1)

            self.cfg["project_prefix"] = chuck_setup.project_prefix
            self.cfg["project_name"] = chuck_setup.project_name
            self.cfg["django_settings"] = chuck_setup.django_settings

            self.inject_variables_and_functions(chuck_setup)

        # No chuck_setup file was found
        else:
            print "\n>>> Cannot find chuck_setup file " + chuck_setup_file
            answer = raw_input("Do you want to continue anyway? (Y/n): ")

            if answer.lower() == "n":
                if os.path.exists(cfg["checkout_destdir"]):
                    shutil.rmtree(cfg["checkout_destdir"])

                sys.exit(1)
            else:
                if not cfg.get("project_prefix"):
                    cfg["project_prefix"] = raw_input("Site: ")

                if not cfg.get("project_name"):
                    cfg["project_name"] = raw_input("Project: ")

                if not cfg.get("django_settings"):
                    default_settings = cfg["project_name"] + ".settings.sites.default.dev.developer_example"
                    cfg["django_settings"] = raw_input("Django settings(" + default_settings + "): ")

                    if not cfg["django_settings"]:
                        cfg["django_settings"] = default_settings

            chuck_setup = None


        # Check if project already exists
        if os.path.exists(self.site_dir) or os.path.exists(self.virtualenv_dir):
            print "Project already exists!"
            answer = raw_input("Remove it? (y/N): ")

            if answer.lower() == "y" or answer.lower() == "j":
                if os.path.exists(self.virtualenv_dir):
                    shutil.rmtree(self.virtualenv_dir)

                if os.path.exists(self.site_dir):
                    shutil.rmtree(self.site_dir)
            else:
                print "Please remove or rename the project and virtualenv before rerun."
                print "\nVirtualenv: " + self.virtualenv_dir
                print "Project: " + self.site_dir
                sys.exit(1)

        # Otherwise move source checkout
        shutil.move(self.checkout_destdir, self.site_dir)

        if chuck_setup and getattr(chuck_setup, "post_git_clone"):
            chuck_setup.post_git_clone()

        # Build Virtualenv
        if chuck_setup and getattr(chuck_setup, "pre_build_virtualenv"):
            chuck_setup.pre_build_virtualenv()

        create_virtualenv.Command().handle(args, cfg)
        install_virtualenv.Command().handle(args, cfg)

        if chuck_setup and getattr(chuck_setup, "post_build_virtualenv"):
            chuck_setup.post_build_virtualenv()


        # Create database
        os.chdir(self.site_dir)

        if not os.path.exists(os.path.join(self.site_dir, "db")):
            os.makedirs(os.path.join(self.site_dir, "db"))

        if chuck_setup and getattr(chuck_setup, "pre_sync_db"):
            chuck_setup.pre_sync_db()

        if chuck_setup and getattr(chuck_setup, "extra_syncdb_options") and chuck_setup.extra_syncdb_options:
            cfg["extra_syncdb_options"] = chuck_setup.extra_syncdb_options

        if chuck_setup and getattr(chuck_setup, "extra_migrate_options") and chuck_setup.extra_migrate_options:
            cfg["extra_migrate_options"] = chuck_setup.extra_migrate_options

        sync_database.Command().handle(args, cfg)

        if chuck_setup and getattr(chuck_setup, "post_sync_db"):
            chuck_setup.post_sync_db()

        if chuck_setup and getattr(chuck_setup, "pre_migrate_db"):
            chuck_setup.pre_migrate_db()


        migrate_database.Command().handle(args, cfg)

        if chuck_setup and getattr(chuck_setup, "post_migrate_db"):
            chuck_setup.post_migrate_db()


        self.print_header("SUMMARY")
        print "\nCloned project " + self.site_dir + " from " + self.checkout_url

        if self.use_virtualenvwrapper:
            print "\nworkon " + self.site_name
        else:
            print "\nsource " + os.path.join(self.virtualenv_dir, "bin", "activate")

        print "cd " + self.site_dir
        print "django-admin.py runserver"
