import os
import sys
import functools
import django_chuck


def get_files(dir):
    """
    Recursivly read a directory and return list of all files
    """
    files = []

    for (path, subdirs, new_files) in os.walk(dir):
        for new_file in new_files:
            files.append(os.path.join(path, new_file))

    return files


def write_to_file(out_file, data):
    """
    copy data to out_file
    """
    if os.access(out_file, os.W_OK):
        out = open(out_file, "wb")
    else:
        if not os.path.exists(os.path.dirname(out_file)):
            os.makedirs(os.path.dirname(out_file))

        out = open(out_file, "wb")

    out.write(data)
    out.close()


def append_to_file(out_file, data):
    """
    append data to out_file
    """
    if os.access(out_file, os.W_OK):
        out = open(out_file, "ab")
    else:
        if not os.path.exists(os.path.dirname(out_file)):
            os.makedirs(os.path.dirname(out_file))

        out = open(out_file, "ab")

    out.write(data)
    out.close()



def find_chuck_module_path():
    """
    Return path to chuck modules
    """
    return os.path.join(sys.prefix, "share", "django_chuck", "modules")


def find_chuck_command_path():
    """
    Search for path to chuck commands in sys.path
    """
    module_path = None

    for path in sys.path:
        full_path = os.path.join(path, "django_chuck", "commands")

        if os.path.exists(full_path):
            module_path = full_path
            break

    return module_path


def find_commands():
    """
    Find all django chuck commands and create a list of module names
    """
    commands = []
    command_path = find_chuck_command_path()

    if command_path:
        for f in os.listdir(command_path):
            if not f.startswith("_") and f.endswith(".py") and \
               not f == "base.py" and not f == "test.py":
                commands.append(f[:-3])

    return commands


def autoload_commands(subparsers, cfg, command_list):
    """
    Load all commands in command_list and create argument parsers
    """
    for cmd_name in command_list:
        module_name = "django_chuck.commands." + cmd_name
        __import__(module_name)

        if getattr(sys.modules[module_name], "Command"):
            cmd = sys.modules[module_name].Command()
            cmd_parser = subparsers.add_parser(cmd_name, help=cmd.help)

            try:
                for arg in cmd.opts:
                    cmd_parser.add_argument(arg[0], **arg[1])
            except TypeError, e:
                print "Broken argument configuration in command " + cmd_name + " argument " + str(arg)
                print str(e)
                sys.exit(0)


            handle_cmd = functools.partial(cmd.handle, cfg=cfg)
            cmd_parser.set_defaults(func=handle_cmd)

    return True


def get_template_engine(site_dir, project_dir, engine_module=None):
    """
    Get template engine instance
    """
    default_engine = "django_chuck.template.notch_interactive.engine"

    if not engine_module:
        engine_module = default_engine

    try:
        __import__(engine_module)
    except Exception, e:
        print "\n<<< Cannot import template engine " + engine_module
        print e
        sys.exit(0)

    if getattr(sys.modules[engine_module], "TemplateEngine"):
        engine = sys.modules[engine_module].TemplateEngine(site_dir, project_dir)
    else:
        print "<<< Template engine " + engine_module + " must implement class TemplateEngine"
        sys.exit(0)

    return engine


def compile_template(input_file, output_file, placeholder, site_dir, project_dir, engine_obj=None, debug=False):
    """
    Load the template engine and let it deal with the output_file
    Parameter: name of template file, dictionary of placeholder name / value pairs, name of template engine module
    """
    result = True

    if output_file.endswith(".pyc") or \
       output_file.endswith(".mo"):
        return None

    if issubclass(engine_obj.__class__, django_chuck.template.base.BaseEngine):
        engine = engine_obj
    else:
        engine = get_template_engine(site_dir, project_dir)

    try:
        engine.handle(input_file, output_file, placeholder)
    except django_chuck.exceptions.TemplateError, e:
        print "\n<<< TEMPLATE ERROR in file " + input_file + "\n"
        print str(e) + "\n"
        result = False

    return result
