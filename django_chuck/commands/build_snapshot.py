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
            if not "==" in line:
                continue

            (app, version) = line.split("==")
            self.requirements[app] = version


        self.update_requirement_file(os.path.join(self.site_dir, 'requirements/requirements_local.txt'))
        self.update_requirement_file(os.path.join(self.site_dir, 'requirements/requirements_dev.txt'))
        self.update_requirement_file(os.path.join(self.site_dir, 'requirements/requirements_live.txt'))
        self.replace_requirement_file(os.path.join(self.site_dir, 'requirements/requirements.txt'))

    def update_requirement_file(self, file):
        for line in fileinput.input(file, inplace=1):
            if line.find('>=') > 0:
                (app,version) = line.split('>=')
            elif line.find('<=') > 0:
                (app,version) = line.split('<=')
            elif line.find('==') > 0:
                (app,version) = line.split('==')
            else:
                print line
                continue

            if self.requirements.get(app):
                print "%s==%s\n" % (app, self.requirements[app]),
                del self.requirements[app]


    def replace_requirement_file(self, file):
        print "Updating " + file
        f = open(file, 'w+')
        f.truncate()
        s = '\n'.join(['%s%s'% (app_name, self.requirements[app_name]) for app_name in self.requirements])
        f.write(s)
        f.close()