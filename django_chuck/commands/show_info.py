import os
from django_chuck.commands.base import BaseCommand
import imp

class Command(BaseCommand):
    help = "Shows all available information of a module"

    def __init__(self):
        super(Command, self).__init__()

        # Disable default checks because this command isn't project-related
        self.no_default_checks = True

        # The module name argument's definition
        self.opts= (("module", {
            "help": "A module name",
            "default": None,
            "nargs": "?",
        }), )

    def show_info(self, module, module_dir):

        self.print_header("Module '%s'" % module)

        print "Location: \t%s" % module_dir

        # Determine chuck_module.py's path
        chuck_module_file = os.path.join(module_dir, "chuck_module.py")

        # Checks whether chuck_module.py exists for this module
        if os.access(chuck_module_file, os.R_OK):
            # Import chuck_module.py as <module_name>
            chuck_module = imp.load_source(module.replace("-", "_"), chuck_module_file)

            # Print dependencies if present
            if hasattr(chuck_module, 'depends'):
                print "Dependencies: \t %s" % ', '.join(chuck_module.depends)

            # Print description if present
            if hasattr(chuck_module, 'description'):
                print chuck_module.description

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)

        module = self.arg_or_cfg('module')

        # Abort if no module name is given.
        if not module:
            print "Please provide a module name!"
            return

        # Iterate over available directories
        module_dir = None
        for module_basedir in self.module_basedirs:
            if module in os.listdir(module_basedir):
                module_dir = os.path.join(module_basedir, module)
                break

        # Abort if no module with the given name exists.
        if not module_dir:
            print "No module with name '%s' found!" % module
            return

        self.show_info(module, module_dir)


