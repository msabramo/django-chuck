import pdb
import subprocess
import re
import os
import sys
from signal import signal, SIGINT, SIGILL, SIGTERM, SIGSEGV, SIGABRT, SIGQUIT
import shutil
import functools
from random import choice
from django_chuck.base.modules import BaseModule


# The base class for all commands

class BaseCommand(object):
    help = "The base class of all chuck commands"

    def got_killed(self, signum=2, frame=None):
        killed_msgs = [
            "Chuck killed Death!",
            "Chuck's going on vacation.",
            "G0t killed by user.",
        ]

        print "\n\n<<< " + choice(killed_msgs)

#        if self.delete_project_on_failure or not getattr(self, "delete_project_on_failure"):
#            if os.path.exists(self.site_dir):
#                print "Deleting project data " + self.site_dir
#                shutil.rmtree(self.site_dir)
#
#            if os.path.exists(self.virtualenv_dir):
#                print "Deleting virtualenv " + self.virtualenv_dir
#                shutil.rmtree(self.virtualenv_dir)
#
#            self.signal_handler()

        sys.exit(1)


    def signal_handler(self):
        """
        Implement this method in your command if you want to do some cleanup
        after being terminated by the user or killed by the system.
        Project and virtualenv dir will get erased automatically.
        """
        pass


    def __init__(self):
        signal(SIGINT, self.got_killed)
        signal(SIGQUIT, self.got_killed)
        signal(SIGILL, self.got_killed)
        signal(SIGABRT, self.got_killed)
        signal(SIGSEGV, self.got_killed)
        signal(SIGTERM, self.got_killed)

        # command arguments will override cfg
        self.args = None

        # config settings
        self.cfg = None

        # dont check that project prefix and name exist?
        self.no_default_checks = False

        # default options
        self.opts = [
            ("project_prefix", {
                "help": "A prefix for the project e.g. customer name. Used to distinguish between site and project dir",
                "default": None,
                "nargs": "?",
            }),

            ("project_name", {
                "help": "The name of the project",
                "default": None,
                "nargs": "?",
            }),

            ("-D", {
                "help": "debug mode",
                "dest": "debug",
                "default": False,
                "action": "store_true",
            }),

            ("-ed", {
                "help": "Your email domain",
                "dest": "email_domain",
                "default": "localhost",
                "nargs": "?",
            }),

            ("-mbs", {
                "help": "Comma separated list of dirs where chuck should look for modules",
                "dest": "module_basedir",
                "default": None,
                "nargs": "?",
            }),

            ("-pb", {
                "help": "The directory where all your projects are stored",
                "dest": "project_basedir",
                "default": None,
                "nargs": "?",
            }),

            ("-pyv", {
                "help": "Python version",
                "dest": "python_version",
                "type": float,
                "default": None,
                "nargs": "?",
            }),

            ("-s", {
                "help": "Django settings module to use after loading virtualenv",
                "dest": "django_settings",
                "default": None,
                "nargs": "?",
            }),

            ("-spb", {
                "help": "The directory on your server where all your projects are stored",
                "dest": "server_project_basedir",
                "default": None,
                "nargs": "?",
            }),

            ("-svb", {
                "help": "The directory on your server where all your virtualenvs are stored",
                "dest": "server_virtualenv_basedir",
                "default": None,
                "nargs": "?",
            }),

            ("-vb", {
                "help": "The directory where all your virtualenvs are stored",
                "dest": "virtualenv_basedir",
                "default": None,
                "nargs": "?",
            }),

            ("-vcs", {
                "help": "Version control system (git, cvs, svn or hg))",
                "dest": "version_control_system",
                "default": "git",
                "nargs": "?",
            }),

            ("-w", {
                "help": "User virtualenv wrapper to create virtualenv",
                "dest": "use_virtualenvwrapper",
                "default": False,
                "action": "store_true",
            }),
        ]


    def arg_or_cfg(self, var):
        """
        Get the value of an parameter or config setting
        """
        try:
            result = getattr(self.args, var)
        except AttributeError:
            result = None

        if not result:
            result = self.cfg.get(var, "")

        return result


    def insert_default_modules(self, module_list):
        """
        Add default modules to your module list
        Ensure that core module is the first module to install
        """
        if self.default_modules:
            for module in reversed(self.default_modules):
                if module not in module_list:
                    module_list.insert(0, module)

        if "core" in module_list:
            del module_list[module_list.index("core")]

        module_list.insert(0, "core")

        return module_list


    def get_install_modules(self):
        """
        Get list of modules to install
        Will insert default module set and resolve module aliases
        """
        try:
            install_modules = re.split("\s*,\s*", self.args.modules)
        except AttributeError:
            install_modules = []
        except TypeError:
            install_modules = []

        install_modules = self.insert_default_modules(install_modules)

        if self.cfg.get("module_aliases"):
            for (module_alias, module_list) in self.cfg.get("module_aliases").items():
                if module_alias in install_modules:
                    module_index = install_modules.index(module_alias)
                    install_modules.pop(module_index)

                    for module in reversed(module_list):
                        install_modules.insert(module_index, module)

        return install_modules

    def get_module_cache(self):
        # Create module dir cache
        module_cache = {}
        for module_basedir in self.module_basedirs:
            for module in os.listdir(module_basedir):
                module_dir = os.path.join(module_basedir, module)

                if os.path.isdir(module_dir) and module not in self.module_cache.keys():
                    module_cache[module] = BaseModule(module, module_dir)
        return module_cache

    def clean_module_list(self, module_list, module_cache):

        errors = []

        # Add dependencies
        def get_dependencies(module_list):
            to_append = []
            for module_name in module_list:
                module = module_cache.get(module_name)
                if module.dependencies:
                    for module_name in module.dependencies:
                        if not module_name in module_list:
                            to_append.append(module_name)
            return to_append

        to_append = get_dependencies(module_list)
        while len(to_append) > 0:
            module_list += to_append
            to_append = get_dependencies(module_list)

        # Check incompatibilities
        for module_name in module_list:
            module = module_cache.get(module_name)
            if module.incompatibles:
                for module_name in module.incompatibles:
                    if module_name in module_list:
                        errors.append("Module %s is not compatible with module %s" % (module.name, module_name))

        if len(errors) > 0:
            print "\n<<< ".join(errors)
            self.kill_system()

        # Order by priority

        module_list = sorted(module_list, key=lambda module: module_cache.get(module).priority)
        return module_list



    def execute_in_project(self, cmd, return_result=False):
        """
        Execute a shell command after loading virtualenv and loading django settings.
        Parameter return_result decides whether the shell command output should get
        printed out or returned.
        """
        commands = self.get_virtualenv_setup_commands(cmd)
        kwargs = dict(
            shell=True,
            stderr=subprocess.PIPE
        )
        if return_result:
            kwargs['stdout'] = subprocess.PIPE

        process = subprocess.Popen(' && '.join(commands), **kwargs)
        stdout, stderr = process.communicate()

        if stderr:
            print stderr
            self.kill_system()
        if return_result:
            return stdout


    def get_virtualenv_setup_commands(self, cmd):
        if self.use_virtualenvwrapper:
            commands = [
                'source ' + os.path.join(os.path.expanduser(self.virtualenv_dir), "bin", "activate"),
                'export DJANGO_SETTINGS_MODULE=' + self.django_settings
                ]
        else:
            commands = [
                'source virtualenvwrapper.sh',
                'workon " + self.site_name',
                'export DJANGO_SETTINGS_MODULE=' + self.django_settings
                ]
        commands.append(cmd)
        return commands


    def db_cleanup(self):
        """
        Sync and migrate, delete content types and load fixtures afterwards
        This is for example useful for complete django-cms migrations
        NOTE: This command will not erase your old database!
        """
        # os.chdir(self.site_dir)
        # sys.path.append(self.site_dir)

        # os.environ["DJANGO_SETTINGS_MODULE"] = self.django_settings
        # # __import__(self.django_settings)
        # # #settings.configure(default_settings=self.django_settings)

        # #from django.utils.importlib import import_module
        # #import_module(self.django_settings)

        # from django.db import connection, transaction
        # from django.conf import settings

        # cursor = connection.cursor()

        # if settings.DATABASE_ENGINE.startswith("postgresql"):
        #     cursor.execute("truncate django_content_type cascade;")
        # else:
        #     cursor.execute("DELETE FROM auth_permission;")
        #     cursor.execute("DELETE FROM django_admin_log;")
        #     cursor.execute("DELETE FROM auth_user;")
        #     cursor.execute("DELETE FROM auth_group_permissions;")
        #     cursor.execute("DELETE FROM auth_user_user_permissions;")
        #     cursor.execute("DELETE FROM django_content_type;")
        #     cursor.execute("DELETE FROM django_site;")
        #     cursor.execute("DELETE FROM south_migrationhistory;")

        # transaction.commit_unless_managed()
        # sys.path.pop()

        cmd = """DELETE FROM auth_permission;
        DELETE FROM django_admin_log;
        DELETE FROM auth_user;
        DELETE FROM auth_group_permissions;
        DELETE FROM auth_user_user_permissions;
        DELETE FROM django_content_type;
        DELETE FROM django_site;
        DELETE FROM south_migrationhistory;"""

        self.execute_in_project("echo '" + cmd + "' | django-admin.py dbshell")


    def load_fixtures(self, fixture_file):
        """
        Load a fixtures file
        """
        self.execute_in_project("django-admin.py loaddata " + fixture_file)


    def __getattr__(self, name):
        """
        Get value either from command-line argument or config setting
        """
        result = None

        if name == "cfg":
            result = self.cfg
        elif name == "args":
            result = self.args

        elif name == "project_prefix":
            result = self.arg_or_cfg(name).replace("-", "_")

        elif name == "project_name":
            result = self.arg_or_cfg(name).replace("-", "_")

        elif name == "virtualenv_dir":
            result = os.path.join(os.path.expanduser(self.virtualenv_basedir), self.project_prefix + "-" + self.project_name)

        elif name == "site_dir":
            result = os.path.join(os.path.expanduser(self.project_basedir), self.project_prefix + "-" + self.project_name)

        elif name == "project_dir":
            result = os.path.join(self.site_dir, self.project_name)

        elif name == "delete_project_on_failure":
            result = self.arg_or_cfg(name)

        elif name == "server_project_basedir":
            result = self.arg_or_cfg(name)

            if not result:
                result = "CHANGEME"

        elif name == "server_virtualenv_basedir":
            result = self.arg_or_cfg(name)

            if not result:
                result = "CHANGEME"

        elif name == "django_settings":
            result = self.arg_or_cfg(name)

            if result and not result.startswith(self.project_name):
                result = self.project_name + "." + result
            elif not result:
                result = self.project_name + ".settings.dev"

        elif name == "site_name":
            result = self.project_prefix + "-" + self.project_name

        elif name == "python_version":
            result = self.arg_or_cfg(name)

            if not result:
                result = sys.version[0:3]

        elif name == "module_basedirs":
            result = self.arg_or_cfg(name)

            if result:
                result[result.index(".")] = self.module_basedir
            else:
                result = [self.module_basedir]

        else:
            result = self.arg_or_cfg(name)

        return result


    def print_header(self, msg):
        """
        Print a header message
        """
        print "\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        print msg
        print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"


    def kill_system(self):
        """
        Your computer failed! Let it die!
        """
        msgs = [
            "Your system gave an Chuck incompatible answer!",
            "The system failed to obey Chuck! Terminate!",
            "Chuck stumbled over his feet and the world fell apart.",
            "Your computer lied to Chuck. Now it tastes a roundhouse-kick!",
            "That was a serious failure. May god forgive Chuck doesnt!",
            "Death to the system for being so faulty!",
        ]

        print "\n<<< " + choice(msgs)
        self.got_killed()


    def inject_variables_and_functions(self, victim_class):
        """
        Inject variables and functions to a class
        Used for chuck_setup and chuck_module helpers
        """
        # inject variables
        setattr(victim_class, "virtualenv_dir", self.virtualenv_dir)
        setattr(victim_class, "site_dir", self.site_dir)
        setattr(victim_class, "project_dir", os.path.join(self.site_dir, self.project_name))
        setattr(victim_class, "project_name", self.project_name)
        setattr(victim_class, "site_name", self.site_name)

        # inject functions
        setattr(victim_class, "execute_in_project", self.execute_in_project)
        setattr(victim_class, "db_cleanup", self.db_cleanup)
        setattr(victim_class, "load_fixtures", self.load_fixtures)

        return victim_class


    def handle(self, args, cfg):
        """
        This method includes the commands functionality
        """
        self.args = args
        self.cfg = cfg

        if not self.no_default_checks:
            if not self.project_prefix:
                raise ValueError("project_prefix is not defined")

            if not self.project_name:
                raise ValueError("project_name is not defined")
