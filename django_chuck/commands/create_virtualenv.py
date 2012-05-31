import subprocess
from django_chuck.commands.base import BaseCommand
import os
import shutil

class Command(BaseCommand):
    help = "Create virtualenv"

    def __init__(self):
        super(Command, self).__init__()


    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        if os.path.exists(self.virtualenv_dir):
            answer = raw_input("Delete old virtualenv dir? <y/N>: ")

            if not answer.lower() == "y" and not answer.lower() == "j":
                print "Aborting."
                return 0

            shutil.rmtree(self.virtualenv_dir)
            os.makedirs(self.virtualenv_dir)
        else:
            os.makedirs(self.virtualenv_dir)


        self.print_header("CREATE VIRTUALENV")

        if self.use_virtualenvwrapper:
            subprocess.call("source virtualenvwrapper.sh; mkvirtualenv --no-site-packages " + self.site_name, shell=True)
            export_dest = open(os.path.join(self.virtualenv_dir, "bin", "postactivate"), "a")
        else:
            subprocess.call("virtualenv --no-site-packages " + self.virtualenv_dir, shell=True)
            export_dest = open(os.path.join(self.virtualenv_dir, "bin", "activate"), "a")

        self.print_header("SETUP VIRTUALENV")

        print "Destination: %s" % export_dest.name
        print "Project path: %s" % "export PYTHONPATH=\"" + self.site_dir + "\":$PYTHONPATH"
        export_dest.write("export PYTHONPATH=\"" + self.site_dir + "\":$PYTHONPATH\n")
        if self.django_settings:
            print "Project settings: %s" % "export DJANGO_SETTINGS_MODULE=" + self.django_settings + "\n"
            export_dest.write("export DJANGO_SETTINGS_MODULE=" + self.django_settings + "\n")
        export_dest.close()