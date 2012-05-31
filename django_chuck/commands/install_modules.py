from django_chuck.commands.base import BaseCommand
import os
import sys
import shutil
from django_chuck.utils import append_to_file, get_files, get_template_engine, compile_template
from random import choice
import imp

class Command(BaseCommand):
    help = "Create all modules"

    # Which modules shall be installed
    modules_to_install = []

    # Remember which module were already installed
    installed_modules = []

    # Remember where we can find which module
    module_cache = {}

    # Post build actions
    post_build_actions = []


    def __init__(self):
        super(Command, self).__init__()

        self.opts.append(("modules", {
            "help": "Comma seperated list of module names (can include pip modules)",
            "default": "core",
            "nargs": "?",
        }))


    def install_module(self, module, as_dependency=False):
        module_dir = self.module_cache.get(module)

        if not module_dir or module in self.installed_modules:
            return

        # Try to read chuck_module.py
        chuck_module_file = os.path.join(module_dir, "chuck_module.py")

        if os.access(chuck_module_file, os.R_OK):
            chuck_module = imp.load_source(module.replace("-", "_"), chuck_module_file)

            # Module has dependencies? Install them first
            if hasattr(chuck_module, "depends"):
                for dep_module in chuck_module.depends:
                    if dep_module not in self.installed_modules:
                        self.modules_to_install.append(dep_module)
                        self.install_module(dep_module, True)

            # Module has post build action? Remember it
            if hasattr(chuck_module, "post_build"):
                chuck_module = self.inject_variables_and_functions(chuck_module)
                setattr(chuck_module, "installed_modules", self.installed_modules)
                self.post_build_actions.append((module, chuck_module.post_build))


        if as_dependency:
            self.print_header("INSTALLING " + module + " AS DEPENDENCY")
        else:
            self.print_header("BUILDING " + module)


        self.installed_modules.append(module)

        # For each file in the module dir
        for f in get_files(module_dir):
            if not "chuck_module.py" in f:
                # Absolute path to module file
                input_file = f

                # Relative path to module file
                rel_path_old = f.replace(module_dir, "")

                # Relative path to module file with project_name replaced
                rel_path_new = f.replace(module_dir, "").replace("project", self.project_name)

                # Absolute path to module file in site dir
                output_file = f.replace(module_dir, self.site_dir).replace(rel_path_old, rel_path_new)

                # Apply templates
                print "\t%s -> %s" % (input_file, output_file)
                compile_template(input_file, output_file, self.placeholder, self.site_dir, self.project_dir, self.template_engine, self.debug)

        if module == "core":
            secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@%^&*(-_=+)') for i in range(50)])
            shutil.move(os.path.join(self.site_dir, ".gitignore_" + self.project_name), os.path.join(self.site_dir, ".gitignore"))
            append_to_file(os.path.join(self.project_dir, "settings", "common.py"), "\nSECRET_KEY = '" + secret_key + "'\n")

        if os.access(chuck_module_file, os.R_OK):
            sys.path.pop(0)


    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)
        self.installed_modules = []
        template_engine = get_template_engine(self.site_dir, self.project_dir, cfg.get("template_engine"))
        self.placeholder = {
            "PROJECT_PREFIX": self.project_prefix,
            "PROJECT_NAME": self.project_name,
            "SITE_NAME": self.site_name,
            "MODULE_BASEDIR": self.module_basedir,
            "PYTHON_VERSION": self.python_version,
            "PROJECT_BASEDIR": self.project_basedir,
            "VIRTUALENV_BASEDIR": self.virtualenv_basedir,
            "SERVER_PROJECT_BASEDIR": self.server_project_basedir,
            "SERVER_VIRTUALENV_BASEDIR": self.server_virtualenv_basedir,
            "EMAIL_DOMAIN": self.email_domain,
        }


        # Project exists
        if os.path.exists(self.site_dir) and not cfg.get("updating"):
            self.print_header("EXISTING PROJECT " + self.site_dir)
            answer = raw_input("Delete old project dir? <y/N>: ")

            if answer.lower() == "y" or answer.lower() == "j":
                shutil.rmtree(self.site_dir)
                os.makedirs(self.site_dir)
            else:
                print "Aborting."
                sys.exit(0)

        # Building a new project
        else:
            os.makedirs(self.site_dir)


        # Which modules shall we install?
        self.modules_to_install = self.get_install_modules()

        # Create module dir cache
        for module_basedir in self.module_basedirs:
            for module in os.listdir(module_basedir):
                module_dir = os.path.join(module_basedir, module)

                if os.path.isdir(module_dir) and module not in self.module_cache.keys():
                    self.module_cache[module] = module_dir

        # Install each module
        for module in self.modules_to_install:
            self.install_module(module)

        not_installed_modules = [m for m in self.modules_to_install if not m in self.installed_modules]

        if not_installed_modules:
            print "\n<<< The following modules cannot be found " + ",".join(not_installed_modules)
            self.kill_system()

        # we are using notch interactive template engine
        # so we want to remove all chuck keywords after successful build
        if (self.template_engine == "django_chuck.template.notch_interactive.engine" or not self.template_engine) and\
           not self.debug:
            for f in get_files(self.site_dir):
                template_engine.remove_keywords(f)


        # execute post build actions
        if self.post_build_actions:
            self.print_header("EXECUTING POST BUILD ACTIONS")

            for action in self.post_build_actions:
                print ">>> " + action[0]
                try:
                    action[1]()
                    print "\n"
                except Exception, e:
                    print str(e)
                    self.kill_system()


