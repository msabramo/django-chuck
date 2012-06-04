import fileinput
from django_chuck.commands.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Build a snapshot of the project requirements and post_build actions"

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        self.print_header("BUILD SNAPSHOT")
        output = self.execute_in_project('pip freeze', return_result=True).split('\n')

        self.requirements = {}
        for line in output:
            if line == '':
                continue
            (app, version) = line.split('==')
            self.requirements[app] = version

        self.update_requirement_file(os.path.join(self.site_dir, 'requirements/requirements.txt'))
        self.update_requirement_file(os.path.join(self.site_dir, 'requirements/requirements_live.txt'))
        self.update_requirement_file(os.path.join(self.site_dir, 'requirements/requirements_dev.txt'))
        self.update_requirement_file(os.path.join(self.site_dir, 'requirements/requirements_local.txt'))

    def update_requirement_file(self, file):
        for line in fileinput.input(file, inplace=1):
            if line.find('-r') >= 0 or line == '\n':
                print line,
                continue
            if line.find('>') > 0:
                (app, version) = line.split(">=")
            elif line.find('<') > 0:
                (app, version) = line.split("<=")
            elif line.find('=') > 0:
                (app, version) = line.split("==")

            print "%s%s" % (app, self.requirements[app]),

